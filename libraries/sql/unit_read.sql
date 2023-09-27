/*Version 23.07 Script to read unit table information for a specified unit
Parameters: unit
This is used for the following situations:
1)Migrating unit content from local database to server database, or vice versa
*/

SELECT ua_number, width
  FROM Unit
 WHERE ua_number = '{unit}';