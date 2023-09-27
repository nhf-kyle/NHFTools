/*Version 23.07 Script to delete specified obstruction of a specified unit
Parameters: unit, pane number, edge number, offset, width
This is used for the following situations:
1) Deleting an obstruction via GUI
2) Migrating obstruction content from local database to server database, or vice versa
*/

/*Delete obstruction*/
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
DELETE FROM Obstruction
      WHERE id = (SELECT id FROM items);