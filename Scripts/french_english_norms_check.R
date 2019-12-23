library(openxlsx)

flatten_fr <- c()
flatten_eng <- c()

print("@@@ FRENCH WORDS IN FRENCH NORMS @@@")
saint_df <- read.xlsx("../Materials/Saint-Aubin_1999a_Exp1_French.xlsx", colNames=F)
print(dim(saint_df))

row_len <- dim(saint_df)[1]
col_len <- dim(saint_df)[2]

affect_df <- read.xlsx("../Norms/AffectiveNormsFrench/13428_2013_431_MOESM2_ESM.xlsx")
colnames(affect_df)[1:8] <- c("Word", "Translation", "PicSource", "PicNumber",
                         "ValenceMean", "ValenceET", "ArousalMean", "ArousalET")

print(colnames(affect_df))
french_words <- affect_df$Word

out_results <- c()
in_results <- c()

for(i in 1:col_len){
  for(j in 1:row_len){
    flatten_fr <- c(flatten_fr, saint_df[j,i])
    if(saint_df[j,i] %in% french_words){
      in_results <- c(in_results, saint_df[j,i])
    }else{
      out_results <- c(out_results, saint_df[j,i])
    }
  }
}
print('OUT')
print(out_results)

print('IN')
print(in_results)

print('coverage')
print(length(in_results) / (length(in_results)+length(out_results)))

print("@@@ ENGLISH WORDS IN ENGLISH NORMS @@@")
eng_saint_df <- read.xlsx("../Materials/Saint-Aubin_1999a_Exp1.xlsx", colNames=F)
print(dim(eng_saint_df))

row_len <- dim(eng_saint_df)[1]
col_len <- dim(eng_saint_df)[2]

eng_affect_df <- read.csv("../Norms/AffectiveNorms/BRM-emot-submit.csv")
eng_words <- eng_affect_df$Word
print(colnames(eng_affect_df))

out_results <- c()
in_results <- c()

for(i in 1:col_len){
  for(j in 1:row_len){
    flatten_eng <- c(flatten_eng, eng_saint_df[j, i])
    if(eng_saint_df[j,i] %in% eng_words){
      in_results <- c(in_results, eng_saint_df[j,i])
    }else{
      out_results <- c(out_results, eng_saint_df[j,i])
    }
  }
}
print('OUT')
print(out_results)

print('IN')
print(in_results)

print('coverage')
print(length(in_results) / (length(in_results)+length(out_results)))

pairs <- cbind(flatten_fr, flatten_eng)

fr_valence <- c()
for(word in flatten_fr){
  if(word %in% affect_df$Word){
    fr_valence <- c(fr_valence, affect_df[(affect_df$Word == word),]$ValenceMean)
  }else{
    fr_valence <- c(fr_valence, NA)
  }
}

fr_arousal <- c()
for(word in flatten_fr){
  if(word %in% affect_df$Word){
    fr_arousal <- c(fr_arousal, affect_df[(affect_df$Word == word),]$ArousalMean)
  }else{
    fr_arousal <- c(fr_arousal, NA)
  }
}

eng_valence <- c()
for(word in flatten_eng){
  if(word %in% eng_affect_df$Word){
    eng_valence <- c(eng_valence, eng_affect_df[(eng_affect_df$Word == word),]$V.Mean.Sum)
  }else{
    eng_valence <- c(eng_valence, NA)
  }
}

eng_arousal <- c()
for(word in flatten_eng){
  if(word %in% eng_affect_df$Word){
    eng_arousal <- c(eng_arousal, eng_affect_df[(eng_affect_df$Word == word),]$A.Mean.Sum)
  }else{
    eng_arousal <- c(eng_arousal, NA)
  }
}

fr_valence <- as.numeric(fr_valence)
fr_arousal <- as.numeric(fr_arousal)

print("correlation")
print(sum(!is.na(eng_valence * fr_valence)))
print(sum(!is.na(eng_arousal* fr_arousal)))
print('Valence')
print(cor.test(eng_valence, fr_valence, use = "pairwise.complete.obs"))
print('Arousal')
print(cor.test(eng_arousal, fr_arousal, use = "pairwise.complete.obs"))
