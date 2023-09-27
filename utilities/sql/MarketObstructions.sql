/*Get id for all edges that have pigtails (Always Edge 3 of Pane 1 for all Market Units)*/
DECLARE @pigtail_ids TABLE (id INT)
INSERT INTO @pigtail_ids
SELECT Edge.id 
FROM Edge 
INNER JOIN Pane ON Pane.id = Edge.pane_id
INNER JOIN Unit ON Unit.id = Pane.unit_id
WHERE ua_number LIKE '1115%'
AND pane_number = 1
AND edge_number = 3;

/*Get id for all obstructions that already exist for pigtails*/
DECLARE @existing_ids TABLE (id INT)
INSERT INTO @existing_ids
SELECT edge_id
FROM Obstruction 
INNER JOIN Edge ON Edge.id = Obstruction.edge_id
INNER JOIN Pane ON Pane.id = Edge.pane_id
INNER JOIN Unit ON Unit.id = Pane.unit_id
WHERE ua_number LIKE '1115%'
AND pane_number = 1
AND edge_number = 3;

/*Get id for edges with pigtails that don't have obstructions*/
DECLARE @missing_ids TABLE (id INT)
INSERT INTO @missing_ids
SELECT * FROM @pigtail_ids
EXCEPT
SELECT * FROM @existing_ids;

/*Initialize For Loop*/
DECLARE @NumRows INT;
SET @NumRows = (SELECT COUNT(*) FROM @missing_ids);
DECLARE @I INT;
SET @I = 1;

/*Use for loop to add obstructions for all missing ids*/
WHILE @I <= @NumRows
BEGIN
	DECLARE @EID INT;
	SET @EID = (SELECT id FROM (SELECT ROW_NUMBER() OVER (ORDER BY id ASC) AS n, id FROM @missing_ids) AS selection WHERE n = @I);
	INSERT INTO Obstruction (edge_id, search_type, track_type, offset, width)
	VALUES (@EID, 1,1,2510,600)
    SET @I = @I + 1;
END