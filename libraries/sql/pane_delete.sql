/*Version 23.07 Script to delete a specified pane
Parameters: unit, pane number
This is used for the following situations:
1) Deleting a pane via GUI
2) Migrating pane content from local database to server database, or vice versa
*/

/*Delete all obstructions for pane*/
DELETE FROM Obstruction
      WHERE id IN 
          (
     SELECT Obstruction.id AS id
       FROM Obstruction
 INNER JOIN Edge ON Edge.id = Obstruction.edge_id
 INNER JOIN Pane ON Pane.id = Edge.pane_id
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
	    AND pane_number = {pane_number}
		  );
/*Delete all edges for pane*/
DELETE FROM Edge
      WHERE id IN 
          (
     SELECT Edge.id AS id
       FROM Edge
 INNER JOIN Pane ON Pane.id = Edge.pane_id
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
	    AND pane_number = {pane_number}
		  );
/*Delete pane*/
DELETE FROM Pane
      WHERE id IN 
	      (
     SELECT Pane.id AS id
       FROM Pane
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
	    AND pane_number = {pane_number}	  
	      );