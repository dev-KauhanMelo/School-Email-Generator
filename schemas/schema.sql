CREATE TABLE IF NOT EXISTS aluno (
    matricula INTEGER PRIMARY KEY AUTOINCREMENT,
    nome text not null, -- for mySQL, use: varchar(80)
    email text unique not null, -- for mySQL, use: varchar(40)
    serie int not null,
    turma char(1) not null,

    constraint chk_serie check(serie in (1, 2 , 3)),
    constraint chk_turma check(turma in ("A", "B", "C"))
);
