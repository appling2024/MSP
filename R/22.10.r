# pym_h <- read.csv("c:\\Users\\user\\Documents\\GitHub\\MSP\\R\\pym_h.csv", sep=" ")
# pym_l <- read.csv("c:\\Users\\user\\Documents\\GitHub\\MSP\\R\\pym_l.csv", sep=" ")

# shapiro_test_h <- shapiro.test(pym_h$imag)
# shapiro_test_l <- shapiro.test(pym_l$imag)

# cat("\nP-value теста Шапиро-Уилка для pym_h:", shapiro_test_h$p.value, "\n")
# cat("P-value теста Шапиро-Уилка для pym_l:", shapiro_test_l$p.value, "\n")

# if (shapiro_test_h$p.value > 0.05 & shapiro_test_l$p.value > 0.05) {
#   t_test_result <- t.test(pym_h$imag, pym_l$imag, alternative = "greater")
#   cat("\nP-value t-теста:", t_test_result$p.value, "\n")
  
#   if (t_test_result$p.value < 0.05) {
#     cat("Нулевая гипотеза отклонена: значения в pym_h больше, чем в pym_l.\n")
#   } else {
#     cat("Нулевая гипотеза не отклонена: нет статистически значимой разницы между группами.\n")
#   }
  
# } else {
#   wilcox_test_result <- wilcox.test(pym_h$imag, pym_l$imag, alternative = "greater")
#   cat("\nP-value теста Манна-Уитни:", wilcox_test_result$p.value, "\n")
  
#   if (wilcox_test_result$p.value < 0.05) {
#     cat("Нулевая гипотеза отклонена: значения в pym_h больше, чем в pym_l.\n")
#   } else {
#     cat("Нулевая гипотеза не отклонена: нет статистически значимой разницы между группами.\n")
#   }
# }


data <- read.csv("c:\\Users\\user\\Documents\\GitHub\\MSP\\R\\speakers_data.csv", sep=";")

{
boxplot(data$British_speakers, data$American_speakers,
        names = c("British speakers", "American speakers"),
        main = "Boxplot for British and American Speakers",
        ylab = "Reaction Time")
    
t_test_result <- t.test(data$British_speakers, data$American_speakers, paired = TRUE)
    
print(t_test_result)
    
if (t_test_result$p.value < 0.05) {
    cat("Нулевая гипотеза отклонена: одна группа статистически значимо реагирует медленнее.\n")
    if (mean(data$British_speakers) > mean(data$American_speakers)) {
    cat("Британские спикеры реагируют медленнее.\n")
    } else {
    cat("Американские спикеры реагируют медленнее.\n")
    }
} else {
      cat("Нулевая гипотеза не отклонена: нет статистически значимой разницы между группами.\n")
    }
}