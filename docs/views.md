### VIEW para Bater Valores de Movimentação

VIEW que nos permite comparar os valores totais de investimentos e movimentos, usaremos o seguinte SQL:

```sql
CREATE VIEW bater_valores_movimentacao AS
SELECT
    subquery_investimentos.investimento,
    subquery_movimentos.movimento,
    subquery_investimentos.investimento = subquery_movimentos.movimento AS all_right
FROM
    (SELECT SUM(valor_atual) AS investimento FROM investimentos) AS subquery_investimentos,
    (SELECT SUM(valor) AS movimento FROM movimentos) AS subquery_movimentos;
```

### VIEW para contular montante ao longo do tempo

```sql
CREATE OR REPLACE VIEW relacao_montante_tempo AS
SELECT
    data_movimento,
    valor,
    (valor - LAG(valor) OVER (ORDER BY data_movimento)) AS diferenca,
    ((valor - LAG(valor) OVER (ORDER BY data_movimento)) / LAG(valor) OVER (ORDER BY data_movimento)) * 100 AS percentage
FROM
    (SELECT DISTINCT
        data_movimento,
        SUM(valor) OVER (ORDER BY data_movimento ASC) AS valor
    FROM
        movimentos) AS subquery
ORDER BY
    data_movimento;
```