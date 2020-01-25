library(meta)
library(metafor)
library(dmetar)
library(grid)

meta_regression_gro <- function(path, forest_out, funnel_out, results_out){

  df <- read.csv(path)
  x <- df$Dsim - df$Sim
  y <- df$Aso - df$Unaso

  print('For all studies, correlation between SMS and CD')
  print(cor(x,y))

  df <- df[order(df$Study),]

  df <- df[!is.na(df$dz), ]
  df <- df[df$Direction != 'unclear', ]
  between_check <- startsWith(as.character(df$N), 'Bet')
  df <- df[!between_check]
  df$N <- as.numeric(as.character(df$N))


  df_len <- length(df$dz)

  if(df_len >= 10){
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
    
    pdf(funnel_out, width=9, height=6)
    funnel(m.hksj,xlab = "g",studlab = TRUE)   
    dev.off() 

    SMSM <- df$Dsim - df$Sim
    CD <- df$Aso - df$Unaso

    print('SMSM & CD correlation')
    print(cor(SMSM, CD))

    df <- cbind(df, SMSM, CD)

    print(df)

    model1 <- rma(yi = yi,
                  sei = vi,
                  data = df,
                  method = "ML",
                  mods = ~ SMSM,
                  test = "knha")
    print(model1)

    model2 <- rma(yi = yi,
                  sei = vi,
                  data = df,
                  method = "ML",
                  mods = ~ SMSM + CD,
                  test = "knha")

    sink(results_out)
    print('SMSM & CD correlation')
    print(cor(SMSM, CD))
    print(m.hksj)
    print(eggers.test(x = m.hksj))
    print(model1)
    print(model2)
    print(anova(model1, model2))
    sink()
  }
}

meta_regression_gro('./results_SerialRecall_preprocessed.csv',
                    'SerialRecallForest.pdf',
                    'SerialRecallFunnel.pdf',
                    'SerialRecallMetaResults.txt')

meta_regression_gro('./results_SerialReconstruction_preprocessed.csv',
                    'SerialReconstructionForest.pdf',
                    'SerialReconstructionFunnel.pdf',
                    'SerialReconstructionMetaResults.txt')
