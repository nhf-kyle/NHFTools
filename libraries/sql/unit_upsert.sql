/*Version 23.07 Script to upsert specified unit
Parameters: unit, width 
This is used for the following situations:
1)Modifying unit attributes via GUI
2)Migrating unit content from local database to server database, or vice versa
*/

/*If pane does not exist in database, insert it with specified values*/   
INSERT INTO Unit (ua_number, width)
     SELECT '{unit}', {width}
      WHERE NOT EXISTS 
          (
     SELECT 1
       FROM Unit
      WHERE ua_number = '{unit}'  
		  ) ;
/*Otherwise, update existing unit with specified values*/
       WITH items AS
          (
     SELECT id
       FROM Unit
      WHERE ua_number = '{unit}'
		  )	   
     UPDATE Unit
        SET width = {width}
      WHERE id = (SELECT id FROM items)