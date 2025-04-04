CREATE DATABASE MedicalDatabase;
USE MedicalDatabase;

CREATE TABLE Medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Pacients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    address VARCHAR(255)
);

CREATE TABLE Medicine_Pacient (
    id INT AUTO_INCREMENT PRIMARY KEY, -- ID-ul tabelului de legătură (opțional)
    medicine_id INT NOT NULL,
    pacient_id INT NOT NULL,
    dosage VARCHAR(50),
    FOREIGN KEY (medicine_id) REFERENCES Medicines(id) ON DELETE CASCADE,
    FOREIGN KEY (pacient_id) REFERENCES Pacients(id) ON DELETE CASCADE,
    UNIQUE KEY (medicine_id, pacient_id) -- Asigură relația unică între o pereche medicine-pacient
);


INSERT INTO Medicines (name, description, price) VALUES 
('Paracetamol', 'Used for pain relief and fever', 5.99),
('Ibuprofen', 'Nonsteroidal anti-inflammatory drug', 7.49);

INSERT INTO Pacients (name, age, address) VALUES 
('John Doe', 35, '123 Main Street'),
('Jane Smith', 28, '456 Elm Street');


INSERT INTO Medicine_Pacient (medicine_id, pacient_id, dosage) VALUES 
(1, 1, '500mg'),
(2, 1, '200mg'),
(1, 2, '250mg');
