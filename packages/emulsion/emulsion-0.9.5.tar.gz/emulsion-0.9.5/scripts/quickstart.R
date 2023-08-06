library(ggplot2)

data <- read.table('outputs/quickstart/counts.csv', header=TRUE, sep=',')

pdf('img/quickstart-health.pdf')
ggplot(data, ) +
    geom_line(aes(step, M), col='pink') +
    geom_line(aes(step, S), col='gray') +
    geom_line(aes(step, E), col='orange') +
    geom_line(aes(step, I), col='red') +
    geom_line(aes(step, R), col='green') +
    geom_line(aes(step, Q), col='blue') +
    facet_wrap(~ simu_id)
dev.off()

pdf('img/quickstart-life.pdf')
ggplot(data, ) +
    geom_line(aes(step, NP), col='gray') +
    geom_line(aes(step, P), col='green') +
    geom_line(aes(step, N), col='black', lwd=2) +
    facet_wrap(~ simu_id)
dev.off()
