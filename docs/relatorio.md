# Relatório do projeto
- Targe valor indicando ocorrencia de 3.14% de inadimplência para os valores de treino

## Engenharia de Features

### Definições

- Features selecionadas por critério de Comportamento:
    1. Valor de depósito : `amount_416A`	
    2. Balanço de depósito do cliente : `amtdepositbalance_4809441A`
    3. Entrada de depósito : `amtdepositincoming_4809444A`
    4. Saída de depósito : `amtdepositoutgoing_4809442A`
    5. Número de parcelas pagas antes do vencimento nos últimos 24 meses : `amtinstpaidbefduel24m_4187115A`
    6. Numeros de consultas de credito no ultimo ano : `days360_512L`
    7. Maximo numero de dias em debito no ultimo ano : `maxdpdlast12m_727P`

    
- Features selecionadas por critério de Aplicação:
    1. Data de nascimento : `birthdate_87D`
    2. Quantidade de meses com qualquer recebimento (renda) : `cntpmts24_3658933L`
    3. Balanço atual da conta de credito : `credacc_actualbalance_314A`
    4. Balanço maximo da conta de credito anterior : `credacc_maxhisbal_375A` 
    5. Balanço mínimo da conta de credito anterior : `credacc_minhisbal_90A` 
    6. Atual total de debido do cliente : `currdebt_22A`
    7. Atual total de debido da aplicação : `currdebtcredtyperange_828A`
    8. Valor total de outros contratos : `contractsum_5085717L`
    9. Total do pagamento inicial : `downpmt_116A`
    10. Nivel educativo : `education_88M`
    11. Numero de regeiçoes nos ultimos 3 anos : `for3years_128L`
    12. Genero : `gender_992L`