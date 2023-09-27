/*Version 23.07 Script to upsert specified pane of a specified unit
Parameters: unit, pane number, plunge depth
This is used for the following situations:
1) Adding a new empty pane via GUI
2) Modifying pane attribute contents via GUI
3) Migrating pane content from local database to server database, or vice versa
*/

/*If pane does not exist in database, insert it with specified values*/
       WITH items AS
          (
     SELECT id
       FROM Unit
      WHERE ua_number = '{unit}'
		  )	   
INSERT INTO Pane (unit_id, pane_number, plunge_depth)
     SELECT (SELECT id FROM items), {pane_number}, {plunge_depth}
      WHERE NOT EXISTS 
          (
     SELECT 1
       FROM Pane
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'  
        AND pane_number =  {pane_number}
		  ) ;
/*Otherwise, update existing pane with specified values*/
       WITH items AS
          (
     SELECT Pane.id AS id
       FROM Pane
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'  
        AND pane_number =  {pane_number}
		  )	   
     UPDATE Pane
        SET plunge_depth = {plunge_depth}
      WHERE id = (SELECT id FROM items)