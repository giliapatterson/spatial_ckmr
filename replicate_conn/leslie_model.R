C = 1.3
ETA1 = 0.055
ETA2 = 2.80
ETA3 = 0.076

ages = 0:200
p_breed = 1/((1 + exp(-1.264*(ages-5.424))))
survival = 1-exp(-C*((ETA1*ages)^ETA2 + (ETA1*ages)^(1/ETA2) + ETA3*ages))
p_mate = 1/((1+exp(-1.868*(ages - 6.5))))

# Survival greater than about 0
nz_surv <- survival > 10e-4
survival <- survival[nz_surv]
p_breed <- p_breed[nz_surv]
p_mate <- p_mate[nz_surv]
ages <- ages[nz_surv]

plot(ages, survival)
plot(ages, p_breed)
plot(ages, p_mate)

# Leslie matrix for females
# Survival
Surv = diag(survival)
# First row is female breeding probability divided by 2
Fec = matrix(p_breed/2, nrow = 1)
# Leslie matrix
M = rbind(Fec, Surv[1:(nrow(Surv)-1),])
# Find eigenvalues
eigen(M)

