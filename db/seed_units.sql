INSERT INTO units (name, unit_type, path) VALUES
    ('Chancellor''s Office', 'chancellor', 'chancellor');

INSERT INTO units (name, unit_type, path) VALUES
    ('College of Engineering', 'college', 'chancellor.engineering'),
    ('College of Chemistry', 'college', 'chancellor.chemistry'),
    ('Haas School of Business', 'college', 'chancellor.business'),
    ('College of Computing, Data Science, and Computing', 'college', 'chancellor.cdss');

INSERT INTO units (name, unit_type, path) VALUES
    ('Bioengineering Department', 'department', 'chancellor.engineering.bioengineering'),
    ('Materials Science Department', 'department', 'chancellor.engineering.materials_science'),
    ('Mechanical Engineering Department', 'department', 'chancellor.engineering.mechanical_engineering'),
    ('Chemistry Department', 'department', 'chancellor.chemistry.chemistry'),
    ('Biochemistry Department', 'department', 'chancellor.chemistry.biochemistry'),
    ('Business Department', 'department', 'chancellor.business.business'),
    ('Department of Accounting', 'department', 'chancellor.business.accounting'),
    ('Department of Data Science', 'department', 'chancellor.cdss.data_science'),
    ('Department of Computer Science', 'department', 'chancellor.cdss.computer_science');