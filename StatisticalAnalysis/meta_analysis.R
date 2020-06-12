library(meta)
library(metafor)
library(dmetar)
library(grid)

meta_regression_gro <- function(path, forest_out, funnel_out, results_out){

  current_f_name = sub("./", "", path)
  df <- read.csv(path)

  # Select studies with within-subject designs and reporting dzs and directions
  df <- df[order(df$Study),]
  df <- df[!is.na(df$dz), ]
  df <- df[df$Direction != 'unclear', ]
  between_check <- startsWith(as.character(df$N), 'Bet')
  df <- df[!between_check]

  SMS <- df$Dsim - df$Sim
  CD <- df$CONSim - df$CONDsim
  SMS_w2v <- df$W2VSim - df$W2VDsim

  df$N <- as.numeric(as.character(df$N))

  data_for_selected <- data.frame(SMS = SMS,
                                   CD = CD,
                                   SMS_w2v = SMS_w2v)

  df_len <- length(df$dz)

  df <- cbind(df, SMS, SMS_w2v, CD)

  # Forest plot 
  if(df_len >= 9){
    df <- escalc(measure = 'SMCC',
                         m1i = dz,
                         sd1i = rep(1, df_len),
                         ni = N,
                         m2i = rep(0, df_len),
                         sd2i = rep(0, df_len),
                         ri = rep(0, df_len),
                         data = df,
                         slab = Study)

    m.hksj <- metagen(yi,
                      vi,
                      data = df,
                      studlab = paste(Study),
                      comb.fixed = FALSE,
                      comb.random = TRUE,
                      method.tau = "SJ",
                      hakn = TRUE,
                      prediction = TRUE,
                      sm = "SMD")

    pdf(forest_out, width=9, height=6)
    forest.jama <- forest(m.hksj,
                          layout = "JAMA",
                          text.predict = "95% PI",
                          col.predict = "black",
                          xlab = "Standardized Mean Difference (95% CI)",
                          colgap.forest.left = unit(15,"mm"))
    dev.off()

    # Funnel plot
    pdf(funnel_out, width=9, height=6)
    funnel(m.hksj,xlab = "g",studlab = TRUE)   
    dev.off()

    # Egger's test
    sink(results_out)
    print(eggers.test(x = m.hksj))
    print(m.hksj)

    # Meta-regression
    model1_SMS <- rma(yi = yi,
                  sei = vi,
                  data = df,
                  method = "ML",
                  mods = ~ SMS,
                  test = "knha")

    model2_SMS <- rma(yi = yi,
                  sei = vi,
                  data = df,
                  method = "ML",
                  mods = ~ SMS + CD,
                  test = "knha")

    model1_SMS_w2v <- rma(yi = yi,
                      sei = vi,
                      data = df,
                      method = "ML",
                      mods = ~ SMS_w2v,
                      test = "knha")

    model2_SMS_w2v <- rma(yi = yi,
                      sei = vi,
                      data = df,
                      method = "ML",
                      mods = ~ SMS_w2v + CD,
                      test = "knha")

    print("@@@ SMS with our proposed index @@@")
    print(model1_SMS)
    print(model2_SMS)
    print(anova(model1_SMS, model2_SMS))

    print("@@@ SMS with word2vec index @@@")
    print(model1_SMS_w2v)
    print(model2_SMS_w2v)
    print(anova(model1_SMS_w2v, model2_SMS_w2v))

    sink()
  }
}

meta_regression_gro('./results_SerialRecall_preprocessed.csv',
                    '../Fig_Table/SerialRecallForest.pdf',
                    '../Fig_Table/SerialRecallFunnel.pdf',
                    '../Results/SerialRecallMetaResults.txt')
