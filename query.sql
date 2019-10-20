SELECT
      e.[District Name] AS District
    , lkt.subject AS Test
    , [Percentage Standard Exceeded] AS Exceeded
    , [Percentage Standard Met] AS Met
    , [Percentage Standard Nearly Met] AS NearlyMet
    , [Percentage Standard Not Met] AS NotMet
FROM lk_entity_type et
INNER JOIN sbac_entities_2019 e
    ON e.[Type Id] = et.typeid
INNER JOIN sbac_scores_2019 s
    ON e.[County Code] = s.[County Code]
    AND e.[District Code] = s.[District Code]
    AND e.[School Code] = s.[School Code]
INNER JOIN lk_test lkt
    ON lkt.testid = s.[Test Id]
INNER JOIN lk_grade lkg
    ON lkg.grade = s.Grade
WHERE et.description = 'District'
    AND e.[District Name] IN ('Oakland Unified', 'San Francisco Unified')
    AND lkg.description = 'All Grades'