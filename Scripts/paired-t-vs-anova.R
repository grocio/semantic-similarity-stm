# This script shows the compatibility in Paired-t test and Two-way ANOVA for within-participants design data

df <- data.frame(
  score = c(3,3,1,3,5,
            4,3,4,5,7,
            6,6,6,4,8,
            5,7,8,7,9,
            3,5,2,4,6,
            2,6,3,6,4,
            3,2,3,6,5,
            2,3,3,4,6),
  id = factor(rep(1:5, 8)),
  A = factor(c(rep(1,20),rep(2,20))),
  B = factor(rep(c(rep(1,5),rep(2,5),rep(3,5),rep(4,5)),2)))

print('@@@ ANOVA @@@')
summary(aov(score ~ A*B +Error(id+id:A+id:B+id:A:B), data=df))

a1 <- c(3+4+6+5,
        3+3+6+7,
        1+4+6+8,
        3+5+4+7,
        5+7+8+9)

a2 <- c(3+2+3+2,
        5+6+2+3,
        2+3+3+3,
        4+6+6+4,
        6+4+5+6)

print('@@@ paired-t @@@')
print(t.test(a1, a2, paired=T))

# The below is a synopsis of the results

# ANOVA
# ~
# Error: id:A
#           Df Sum Sq Mean Sq F value Pr(>F)
# A          1  16.90  16.900   8.096 0.0466 *
# Residuals  4   8.35   2.087
# ---
# Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
# ~

# Paired-t
# ~
# t = 2.8453, df = 4, p-value = 0.04662
# ~

# First, p values are equivalent in ANOVA and paired-t (0.0466 and 0.04662)
# Second, as sqrt(8.096) = 2.845347, squared root of F value = t value
# Thus, the results show the compatibility in ANOVA and paired-t

# Note. Cohen's dz (effect size) can be calculated as follows:
# t value / sqrt(sample size)
# See Lakens (2013) Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs
