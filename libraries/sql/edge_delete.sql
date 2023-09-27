/*Version 23.07 Script to delete specified edge of a specified unit
Parameters: unit, pane number, edge number
This is used for the following situations:
1) Deleting an edge via GUI
2) Migrating edge content from local database to server database, or vice versa
3) Regenerating edge when changing pane type
*/

/*Delete all obstructions for edge*/
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
		  )
DELETE FROM Obstruction
      WHERE id = (SELECT id FROM items);
/*Delete edge*/
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
DELETE FROM Edge
      WHERE id = (SELECT id FROM items);