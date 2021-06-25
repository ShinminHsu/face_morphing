library(irr)

remove_outliers <- function(x, na.rm = TRUE, ...) {
    qnt <- quantile(x, probs=c(.25, .75), na.rm = na.rm, ...)
    H <- 1.5 * IQR(x, na.rm = na.rm)
    y <- x
    y[x < (qnt[1] - H)] <- NA
    y[x > (qnt[2] + H)] <- NA
    y
}

remove_outliers_wrapper <- function(subset) {

    for (int in c(25, 50, 75, 100)) {
        for (ID in c(16, 18, 21, 23, 38, 58)) {
            for (emo in emotions) {
                
                for (colEmo in emotions){
                    
                    rating = subset[subset$imgInt == int & subset$imgEmo == emo & subset$imgID == ID, colEmo]
                    detect = remove_outliers(rating)
                    
                    if(anyNA(detect)){
                        
                        print(detect)
                        subset[subset$imgInt == int & subset$imgEmo == emo & subset$imgID == ID, colEmo] = detect
                        
                    }    
                }
                
            }
        }
    }
    
    return(subset)
}

compute_all_ratings <- function(df_sort) {
    
    IDs = unique(df_sort$ratersID)
    ratings = data.frame()
    
    for(ID in IDs){
        
        flatten = c()
        
        for (col in emotions) {
            
            subset1 = df_sort[df_sort$ratersID == ID & df_sort$imgEmo == 'neutral', col]
            for (emotion in emotions){
                subset2 = df_sort[df_sort$ratersID == ID & df_sort$imgEmo == emotion, col]    
                flatten = c(flatten, subset2)   
            }
            flatten = c(flatten, subset1)
        }
        
        flatten_df = data.frame(ID=flatten)
        colnames(flatten_df) = ID
        
        if(ncol(ratings) == 0){
            ratings = flatten_df
        }else{
            ratings = cbind(ratings, flatten_df)   
        }   
    }
    
    a = kripp.alpha(t(as.matrix(ratings)), "ordinal")
    return(a)
}

df <- read.csv('human_rating_caucasian.csv')
df <- read.csv('human_rating_taiwanese.csv')


emotions = c('happy', 'sad', 'angry', 'fearful', 'disgusted', 'surprised')
subset = select(df, 'ratersID', 'happy', 'sad', 'angry', 'fearful', 'disgusted', 'surprised', 'imgID', 'imgEmo', 'imgInt')

df = remove_outliers_wrapper(subset)

df_sort = df[order(df$ratersID, df$imgID, df$imgEmo, df$imgInt), ]
rownames(df_sort) <- NULL

all = compute_all_ratings(df_sort)
print(all)

