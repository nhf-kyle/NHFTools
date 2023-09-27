/*Create new obstuction table with addtional 'obstruction number' column*/
CREATE TABLE ObstructionNew (
    id INTEGER NOT NULL PRIMARY KEY IDENTITY(1,1),
    edge_id INTEGER NOT NULL,
	obstruction_number INTEGER NOT NULL DEFAULT 1,
	search_type TINYINT NOT NULL DEFAULT 0,
	track_type TINYINT NOT NULL DEFAULT 0,
	offset REAL NOT NULL DEFAULT 0,
	width REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (edge_id) REFERENCES Edge(id)
);

/*Copy contents of old obstruction table into new obstruction table (while filling in obstuction number with default value)*/
SET IDENTITY_INSERT ObstructionNew ON;
INSERT INTO ObstructionNew (id, edge_id, search_type, track_type, offset, width) SELECT id, edge_id, search_type, track_type, offset, width FROM Obstruction;
SET IDENTITY_INSERT ObstructionNew OFF;

/*Delete old obstruction table*/
DROP TABLE Obstruction;

/*Rename new obstruction table*/
EXEC sp_rename 'ObstructionNew', 'Obstruction'