/*Version 23.07 Script to upsert specified obstruction of a specified unit
Parameters: unit, pane number, edge number, obstruction_number, offset, width
This is used for the following situations:
1) Adding a new empty obstruction via GUI
2) Modifying obstruction attribute contents via GUI
3) Migrating obstruction content from local database to server database, or vice versa
*/

/*If obstruction does not exist in database, insert it with specified values*/
       WITH items AS 
	      (
     SELECT Edge.id AS id 
	   FROM Edge
 INNER JOIN Pane ON Pane.id = Edge.pane_id 
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
        AND pane_number = {pane_number}
        AND edge_number = {edge_number}
          ) 
INSERT INTO Obstruction (edge_id, obstruction_number, search_type, track_type, offset, width)
     SELECT (SELECT id FROM items), {obstruction_number}, {search_type}, {track_type}, {offset}, {width}
	 WHERE NOT EXISTS
	      (
     SELECT 1
	   FROM Obstruction
 INNER JOIN Edge ON Edge.id = Obstruction.edge_id
 INNER JOIN Pane ON Pane.id = Edge.pane_id 
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
        AND pane_number = {pane_number}
        AND edge_number = {edge_number}
		AND obstruction_number = {obstruction_number}
		  ) ;
/*Otherwise, update existing edge with specified values*/
       WITH items AS 
	      (
     SELECT Obstruction.id AS id 
	   FROM Obstruction
 INNER JOIN Edge ON Edge.id = Obstruction.edge_id
 INNER JOIN Pane ON Pane.id = Edge.pane_id 
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
        AND pane_number = {pane_number}
        AND edge_number = {edge_number}
		AND obstruction_number = {obstruction_number}
          ) 
     UPDATE Obstruction
        SET search_type = {search_type},
			track_type = {track_type},
			offset = {offset},
			width = {width}
      WHERE id = (SELECT id FROM items);