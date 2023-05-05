CREATE TABLE voters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fio TEXT NOT NULL,
                    public_key BLOB NOT NULL);

CREATE TABLE elections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    results_true INTEGER);

CREATE TABLE voters_elections_link (
                    id_voter INTEGER,
                    id_election INTEGER,
                    vote TEXT NOT NULL,
                    PRIMARY KEY (id_voter, id_election),
                    FOREIGN KEY (id_voter) REFERENCES voters(id),
                    FOREIGN KEY (id_election) REFERENCES elections(id));



