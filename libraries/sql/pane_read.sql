/*Version 23.07 Script to read pane table information for a specified unit
Parameters: unit
This is used for the following situations:
1)Migrating unit content from local database to server database, or vice versa
*/

    SELECT ua_number, pane_number, plunge_depth
      FROM Pane 
INNER JOIN Unit ON Unit.id = Pane.unit_id
 WHERE ua_number = '{unit}';