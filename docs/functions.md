### FUNCTIONS 

```sql
CREATE OR REPLACE FUNCTION consultar_investimentos(tipo_investimento text)
RETURNS TABLE (tipo_investimento_retorno text, data_movimento date, valor numeric, diferenca numeric, percentage numeric)
AS $$
BEGIN
    RETURN QUERY
    select
        tipo_investimento AS tipo_investimento_retorno,
        subquery.data_movimento,
        subquery.valor,
        (subquery.valor - LAG(subquery.valor) OVER (ORDER BY subquery.data_movimento)) AS diferenca,
        ((subquery.valor - LAG(subquery.valor) OVER (ORDER BY subquery.data_movimento)) / LAG(subquery.valor) OVER (ORDER BY subquery.data_movimento)) * 100 AS percentage
    FROM
        (SELECT DISTINCT
            m.data_movimento,
            SUM(m.valor) OVER (ORDER BY m.data_movimento ASC) AS valor
        FROM
            movimentos m 
        LEFT JOIN investimentos i ON i.id = m.investimento_id 
        WHERE i.tipo = tipo_investimento
        ) AS subquery
    ORDER BY
        subquery.data_movimento;
END;
$$
LANGUAGE plpgsql;

```