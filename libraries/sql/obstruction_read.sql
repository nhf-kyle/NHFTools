/*Version 23.07 Script to read all obstructions for a specified unit
Parameters: unit
This is used for the following situations:
1)Migrating obstruction content from local database to server database, or vice versa
*/

    SELECT pane_number, edge_number, obstruction_number, search_type, track_type, offset, Obstruction.width
      FROM Obstruction	
INNER JOIN Edge ON Edge.id = Obstruction.edge_id 
INNER JOIN Pane ON Pane.id = Edge.pane_id 
INNER JOIN Unit ON Unit.id = Pane.unit_id 
     WHERE ua_number = '{unit}';