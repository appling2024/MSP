pym_h <- read.csv("c:\\Users\\user\\Documents\\GitHub\\MSP\\R\\pym_h.csv", sep=" ")
pym_l <- read.csv("c:\\Users\\user\\Documents\\GitHub\\MSP\\R\\pym_l.csv", sep=" ")

str(pym_h)
str(pym_l)

pym_h$imag <- as.numeric(pym_h$imag)
pym_h$conc <- as.numeric(pym_h$conc)
pym_h$assoc <- as.numeric(pym_h$assoc)

pym_l$imag <- as.numeric(pym_l$imag)
pym_l$conc <- as.numeric(pym_l$conc)
pym_l$assoc <- as.numeric(pym_l$assoc)

t_test_imag <- t.test(pym_h$imag, pym_l$imag, var.equal = FALSE)
t_test_conc <- t.test(pym_h$conc, pym_l$conc, var.equal = FALSE)
t_test_assoc <- t.test(pym_h$assoc, pym_l$assoc, var.equal = FALSE)

print(t_test_imag)
print(t_test_conc)
print(t_test_assoc)

shapiro_test_imag_h <- shapiro.test(pym_h$imag)
shapiro_test_conc_h <- shapiro.test(pym_h$conc)
shapiro_test_assoc_h <- shapiro.test(pym_h$assoc)

shapiro_test_imag_l <- shapiro.test(pym_l$imag)
shapiro_test_conc_l <- shapiro.test(pym_l$conc)
shapiro_test_assoc_l <- shapiro.test(pym_l$assoc)

print(shapiro_test_imag_h)
print(shapiro_test_conc_h)
print(shapiro_test_assoc_h)

print(shapiro_test_imag_l)
print(shapiro_test_conc_l)
print(shapiro_test_assoc_l)

boxplot(pym_h$assoc, pym_l$assoc)
boxplot(pym_h$assoc, pym_l$assoc, names = c("high", "low"), main = "Box plots", xlab = "Frequency group", ylab = "Average number pf associations")