/*Version 23.07 Script to upsert specified edge of a specified unit
Parameters: unit, pane number, edge number, edge type, fill area, x0, y0, z0, x1, y1, z1
This is used for the following situations:
1) Adding a new empty edge via GUI
2) Modifying edge attribute contents via GUI
3) Migrating edge content from local database to server database, or vice versa
*/

/*If edge does not exist in database, insert it with specified values*/
       WITH items AS 
	      (
     SELECT Pane.id AS id 
       FROM Pane
 INNER JOIN Unit u ON u.id = Pane.unit_id
      WHERE ua_number = '{unit}'
        AND pane_number = {pane_number}
          ) 
INSERT INTO Edge (pane_id, edge_number, edge_type, fill_area, x0, y0, z0, x1, y1, z1)
     SELECT (SELECT id FROM items), {edge_number}, {edge_type}, {fill_area}, {x0}, {y0}, {z0}, {x1}, {y1}, {z1}
      WHERE NOT EXISTS
	      (
     SELECT 1
       FROM Edge
 INNER JOIN Pane ON Pane.id = Edge.pane_id 
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
        AND pane_number = {pane_number}
        AND edge_number = {edge_number}
		  ) ;
/*Otherwise, update existing edge with specified values*/
       WITH items AS 
          (
     SELECT Edge.id AS id
       FROM Edge
 INNER JOIN Pane ON Pane.id = Edge.pane_id 
 INNER JOIN Unit ON Unit.id = Pane.unit_id
      WHERE ua_number = '{unit}'
        AND pane_number =  {pane_number}
        AND edge_number = {edge_number}
          )
     UPDATE Edge
        SET edge_type = {edge_type},
			fill_area = {fill_area},
			x0 = {x0},
			y0 = {y0},
			z0 = {z0},
			x1 = {x1},
			y1 = {y1},
			z1 = {z1}
      WHERE id = (SELECT id FROM items);