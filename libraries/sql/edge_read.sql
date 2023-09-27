/*Version 23.07 Script to read all edges for a specified unit
Parameters: unit
This is used for the following situations:
1)Migrating unit content from local database to server database, or vice versa
2)Regenerating edge when changing pane type
*/

    SELECT pane_number, edge_number, width, plunge_depth, edge_type, fill_area, x0, y0, z0, x1, y1, z1
      FROM Edge 
INNER JOIN Pane ON Pane.id = Edge.pane_id 
INNER JOIN Unit ON Unit.id = Pane.unit_id 
     WHERE ua_number = '{unit}';