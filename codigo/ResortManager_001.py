import mysql.connector
from mysql.connector import errorcode
import numpy as np
import matplotlib.pyplot as plt


# Variáveis
# Valores para criação de tabelas do Banco de Dados
tables = {'Resort': (
            """CREATE TABLE Resort (
            Rating INT,
            Address VARCHAR(30),
            Resort_name VARCHAR(30),
            ResortId INT PRIMARY KEY
        )"""),
        'Mountain': (
            """CREATE TABLE Mountain (
            MoutainId INT PRIMARY KEY,
            Number_tracks INT,
            Mountain_name VARCHAR(30),
            Number_lifts INT,
            ResortId INT,
            FOREIGN KEY(ResortId) REFERENCES Resort (ResortId)
        )"""),
        'Facility': (
            """CREATE TABLE Facility (
            FacilityId INT PRIMARY KEY,
            Facility_Description VARCHAR(30),
            ResortID INT,
            FOREIGN KEY(ResortId) REFERENCES Resort (ResortId)
        )"""),
        'Restaurant': (
            """CREATE TABLE Restaurant (
            RestaurantId INT PRIMARY KEY,
            Culinary_type VARCHAR(30),
            Rating INT,
            Address VARCHAR(100),
            Restaurant_name VARCHAR(30),
            FacilityId INT,
            FOREIGN KEY(FacilityId) REFERENCES Facility (FacilityId)
        )"""),
        'Menu': (
            """CREATE TABLE Menu (
            MenuId INT PRIMARY KEY,
            Description VARCHAR(30),
            RestaurantId INT,
            FOREIGN KEY(RestaurantId) REFERENCES Restaurant (RestaurantId)
        )"""),
        'Dish': (
            """CREATE TABLE Dish (
            DishId INT PRIMARY KEY,
            Description VARCHAR(30),
            MenuId INT,
            Dish_Value INT,
            FOREIGN KEY(MenuId) REFERENCES Menu (MenuId)
        )"""),
        'Service': (
            """CREATE TABLE Service (
            Service_description VARCHAR(50),
            ServiceId INT PRIMARY KEY
        )"""),
        'Department': (
            """CREATE TABLE Department (
            DeptId INT PRIMARY KEY,
            Description VARCHAR(30)
        )"""),
        'Role': (
            """CREATE TABLE Role (
            PosId INT PRIMARY KEY,
            Job_Title VARCHAR(30),
            DeptId INT,
            FOREIGN KEY(DeptId) REFERENCES Department (DeptId)
        )"""),
        'Employee': (
            """CREATE TABLE Employee (
            Last_name VARCHAR(30),
            First_name VARCHAR(30),
            Age INT,
            Sex VARCHAR(1),
            EmployeeID INT PRIMARY KEY,
            City_code VARCHAR(5),
            ManagerId INT,
            PosId INT,
            FOREIGN KEY(PosId) REFERENCES Role (PosId)
        )"""),
        'Facility_service': (
            """CREATE TABLE Facility_service (
            FacilityId INT,
            ServiceId INT,
            FOREIGN KEY(FacilityId) REFERENCES Facility (FacilityId),
            FOREIGN KEY(ServiceId) REFERENCES Service (ServiceId)
        )"""),
        'Facility_employee': (
            """CREATE TABLE Facility_employee (
            FacilityId INT,
            EmployeeID INT,
            FOREIGN KEY(FacilityId) REFERENCES Facility (FacilityId),
            FOREIGN KEY(EmployeeID) REFERENCES Employee (EmployeeID)
        )"""),
}

# Valores para serem inseridos no Banco de Dados
inserts = {'Resort': (
    """INSERT INTO Resort (ResortID, Resort_Name, Address, Rating) VALUES
(1, 'Aspen Snowmass', 'Aspen, Colorado', 4),
(2, 'Vail', 'Vail, Colorado', 3),
(3, 'Jackson Hole Mountain Resort', 'Teton Village, Wyoming', 5),
(4, 'Breckenridge', 'Breckenridge, Colorado', 4),
(5, 'Big Sky Resort', 'Big Sky, Montana', 4),
(6, 'Sun Valley Resort', 'Sun Valley, Idaho', 5)"""),
    'Mountain': (
        """INSERT INTO Mountain (MoutainId, Mountain_Name, Number_Tracks, Number_Lifts, ResortId) VALUES
(1, 'Aspen Mountain', 76, 8, 1),
(2, 'Aspen Highlands', 122, 5, 1),
(3, 'Buttermilk', 44, 7, 1),
(4, 'Snowmass Mountain', 96, 20, 1),
(5, 'Vail Mountain', 195, 31, 2),
(6, 'Rendezvous Mountain', 133, 12, 3),
(7, 'Peak 6', 10, 1, 4),
(8, 'Peak 7', 13, 2, 4),
(9, 'Peak 8', 32, 5, 4),
(10, 'Peak 9', 26, 6, 4),
(11, 'Peak 10', 12, 1, 4),
(12, 'Lone Mountain', 300, 36, 5),
(13, 'Bald Mountain', 75, 13, 6),
(14, 'Dollar Mountain', 22, 4, 6)"""),
    'Facility': (
        """INSERT INTO Facility (FacilityID, Facility_Description, ResortId) VALUES
(1, 'Hotel', 1),           
(2, 'Restaurant', 1),      
(3, 'Shop', 1),            
(4, 'Parking', 1),         
(5, 'Hotel', 2),          
(6, 'Restaurant', 2),     
(7, 'Shop', 2),           
(8, 'Parking', 2),        
(9, 'Hotel', 3),          
(10, 'Restaurant', 3),    
(11, 'Shop', 3),          
(12, 'Parking', 3),       
(13, 'Hotel', 4),         
(14, 'Restaurant', 4),    
(15, 'Shop', 4),          
(16, 'Parking', 4),       
(17, 'Hotel', 5),         
(18, 'Restaurant', 5),    
(19, 'Shop', 5),          
(20, 'Parking', 5),       
(21, 'Hotel', 6),        
(22, 'Restaurant', 6),   
(23, 'Shop', 6),         
(24, 'Parking', 6)"""),
    'Service': (
        """INSERT INTO Service (ServiceID, Service_Description) VALUES
(1, 'Room Service'),             
(2, 'Concierge Service'),         
(3, 'Housekeeping'),             
(4, 'Spa Services'),            
(5, 'Restaurant Reservations'),   
(6, 'Ski Rentals'),              
(7, 'Ski Lessons'),              
(8, 'Equipment Repair'),         
(9, 'Guided Tours'),             
(10, 'Parking Assistance'),      
(11, 'Valet Parking'),           
(12, 'Shuttle Service'),         
(13, 'Gourmet Dining'),           
(14, 'Bar Service'),             
(15, 'Takeout'),                 
(16, 'Live Music'),              
(17, 'Event Hosting'),           
(18, 'Childcare'),               
(19, 'Fitness Center'),           
(20, 'WiFi Access'),             
(21, 'Airport Transfer'),         
(22, 'Ski Valet'),               
(23, 'Gift Wrapping'),          
(24, 'Personal Shopping'),       
(25, 'Laundry Service'),         
(26, 'Pet Services'),            
(27, 'Wedding Planning'),        
(28, 'Meeting Facilities'),      
(29, 'Room Upgrade'),            
(30, '24-Hour Front Desk')"""),
    'Facility_Service': (
        """INSERT INTO Facility_Service (FacilityID, ServiceID) VALUES
(1, 1), 
(1, 2), 
(1, 3),
(1, 4),  
(1, 5), 
(1, 18), 
(1, 19), 
(1, 22), 
(1, 25), 
(1, 26), 
(1, 27), 
(1, 28), 
(1, 29), 
(1, 30),
(2, 13), 
(2, 14), 
(2, 15), 
(2, 16), 
(3, 6), 
(3, 7), 
(3, 8), 
(3, 9), 
(3, 23), 
(3, 24), 
(4, 10), 
(4, 11), 
(4, 12),
(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 18), (5, 19), (5, 22), (5, 25), (5, 26), (5, 27), (5, 28), (5, 29), (5, 30),
(6, 13), (6, 14), (6, 15), (6, 16),
(7, 6), (7, 7), (7, 8), (7, 9), (7, 23), (7, 24),
(8, 10), (8, 11), (8, 12),
(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 18), (9, 19), (9, 22), (9, 25), (9, 26), (9, 27), (9, 28), (9, 29), (9, 30),
(10, 13), (10, 14), (10, 15), (10, 16),
(11, 6), (11, 7), (11, 8), (11, 9), (11, 23), (11, 24),
(12, 10), (12, 11), (12, 12),
(13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 18), (13, 19), (13, 22), (13, 25), (13, 26), (13, 27), (13, 28), (13, 29), (13, 30),
(14, 13), (14, 14), (14, 15), (14, 16),
(15, 6), (15, 7), (15, 8), (15, 9), (15, 23), (15, 24),
(16, 10), (16, 11), (16, 12),
(17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 18), (17, 19), (17, 22), (17, 25), (17, 26), (17, 27), (17, 28), (17, 29), (17, 30),
(18, 13), (18, 14), (18, 15), (18, 16),
(19, 6), (19, 7), (19, 8), (19, 9), (19, 23), (19, 24),
(20, 10), (20, 11), (20, 12),
(21, 1), (21, 2), (21, 3), (21, 4), (21, 5), (21, 18), (21, 19), (21, 22), (21, 25), (21, 26), (21, 27), (21, 28), (21, 29), (21, 30),
(22, 13), (22, 14), (22, 15), (22, 16),
(23, 6), (23, 7), (23, 8), (23, 9), (23, 23), (23, 24),
(24, 10), (24, 11), (24, 12)"""),
    'Restaurant': (
        """INSERT INTO Restaurant (RestaurantId, Restaurant_Name, Culinary_Type, Rating, Address, FacilityId) VALUES
(1, 'Element 47', 1, 5, '123 Aspen St, Aspen, CO', 1),
(2, 'The 10th', 2, 4, '456 Vail Rd, Vail, CO', 2),
(3, 'Hearthstone Restaurant', 3, 5, '789 Breckenridge Ave, Breckenridge, CO', 3),
(4, 'Piste Mountain Bistro', 4, 4, '101 Jackson Hole Dr, Teton Village, WY', 4),
(5, 'The Ram', 5, 5, '202 Sun Valley Rd, Sun Valley, ID', 5)"""),
    'Menu': (
        """INSERT INTO Menu (MenuId, Description, RestaurantID) VALUES
(1, 'Breakfast', 1),
(2, 'Lunch', 2),
(3, 'Dinner', 3),
(4, 'Mexican Food', 4),
(5, 'Austrian Food', 5)"""),
    'Dish': (
        """INSERT INTO Dish (DishId, Description, Dish_Value, MenuId) VALUES
    (1, 'Pancakes', 10, 1),
    (2, 'Eggs Benedict', 12, 1),
    (3, 'French Toast', 11, 1),
    (4, 'Breakfast Burrito', 9, 1),
    (5, 'Omelette', 8, 1),
    (6, 'Yogurt Parfait', 7, 1),
    (7, 'Bagel with Cream Cheese', 6, 1),
    (8, 'Smoked Salmon Bagel', 13, 1),
    (9, 'Avocado Toast', 10, 1),
    (10, 'Granola and Fruit', 7, 1),
    (11, 'Breakfast Sandwich', 8, 1),
    (12, 'Waffles', 10, 1),
    (13, 'Caesar Salad', 12, 2),
    (14, 'Club Sandwich', 11, 2),
    (15, 'Grilled Chicken Salad', 13, 2),
    (16, 'Cheeseburger', 14, 2),
    (17, 'Margherita Pizza', 15, 2),
    (18, 'Turkey Wrap', 10, 2),
    (19, 'Fish Tacos', 14, 2),
    (20, 'BLT Sandwich', 11, 2),
    (21, 'Chicken Quesadilla', 12, 2),
    (22, 'Veggie Burger', 13, 2),
    (23, 'Pasta Primavera', 14, 2),
    (24, 'Steak Sandwich', 16, 2),
    (25, 'Grilled Salmon', 20, 3),
    (26, 'Ribeye Steak', 25, 3),
    (27, 'Lobster Tail', 30, 3),
    (28, 'Chicken Alfredo', 18, 3),
    (29, 'Beef Wellington', 35, 3),
    (30, 'Vegetable Stir Fry', 17, 3),
    (31, 'Shrimp Scampi', 22, 3),
    (32, 'Filet Mignon', 28, 3),
    (33, 'Roast Duck', 27, 3),
    (34, 'Lamb Chops', 26, 3),
    (35, 'Pork Tenderloin', 19, 3),
    (36, 'Mushroom Risotto', 18, 3),
    (37, 'Tacos', 12, 4),
    (38, 'Enchiladas', 13, 4),
    (39, 'Guacamole', 10, 4),
    (40, 'Quesadillas', 11, 4),
    (41, 'Churros', 8, 4),
    (42, 'Wiener Schnitzel', 20, 5),
    (43, 'Goulash', 18, 5),
    (44, 'Apfelstrudel', 10, 5),
    (45, 'Kaiserschmarrn', 12, 5),
    (46, 'Sachertorte', 14, 5)"""),
    'Department': (
        """INSERT INTO Department (DeptId, Description) VALUES
    (1, 'Front Desk'),
    (2, 'Housekeeping'),
    (3, 'Food and Beverage'),
    (4, 'Maintenance'),
    (5, 'Ski School'),
    (6, 'Lift Operations'),
    (7, 'Retail'),
    (8, 'Guest Services'),
    (9, 'Marketing'),
    (10, 'Human Resources')"""),
    'Role': (
        """INSERT INTO Role (PosId, Job_Title, DeptId) VALUES
    -- Front Desk (DeptId = 1)
    (1, 'Manager', 1),
    (2, 'Receptionist', 1),
    (3, 'Concierge', 1),
    (4, 'Supervisor', 2),
    (5, 'Room Attendant', 2),
    (6, 'Laundry Staff', 2),
    (7, 'Housekeeper', 2),
    (8, 'Chef', 3),
    (9, 'Waiter', 3),
    (10, 'Bartender', 3),
    (11, 'Cook', 3),
    (12, 'Dishwasher', 3),
    (13, 'Technician', 4),
    (14, 'Electrician', 4),
    (15, 'Plumber', 4),
    (16, 'Instructor', 5),
    (17, 'Assistant', 5),
    (18, 'Supervisor', 5),
    (19, 'Operator', 6),
    (20, 'Mechanic', 6),
    (21, 'Supervisor', 6),
    (22, 'Sales Associate', 7),
    (23, 'Store Manager', 7),
    (24, 'Cashier', 7),
    (25, 'Coordinator', 8),
    (26, 'Representative', 8),
    (27, 'Supervisor', 8),
    (28, 'Coordinator', 9),
    (29, 'Manager', 9),
    (30, 'Assistant', 9),
    (31, 'HR Manager', 10),
    (32, 'Recruiter', 10),
    (33, 'Trainer', 10)"""),
    'Employee': (
        """INSERT INTO Employee (EmployeeId, Last_name, First_name, Age, Sex, ManagerId, PosId, City_code) VALUES
    (1, 'Smith', 'Linda', 18, 'F', 2, 5, 'BAL'),          
    (2, 'Kim', 'Tracy', 19, 'F', NULL, 8, 'HKG'),         
    (3, 'Jones', 'Shiela', 21, 'F', 1, 11, 'WAS'),        
    (4, 'Kumar', 'Dinesh', 20, 'M', 3, 15, 'CHI'),        
    (5, 'Gompers', 'Paul', 26, 'M', NULL, 1, 'YYZ'),      
    (6, 'Schultz', 'Andy', 18, 'M', 7, 7, 'BAL'),         
    (7, 'Apap', 'Lisa', 18, 'F', 6, 7, 'PIT'),            
    (8, 'Nelson', 'Jandy', 20, 'F', 5, 9, 'BAL'),         
    (9, 'Tai', 'Eric', 19, 'M', 1, 19, 'YYZ'),            
    (10, 'Lee', 'Derek', 17, 'M', 4, 19, 'HOU'),          
    (11, 'Adams', 'David', 22, 'M', 2, 14, 'PHL'),        
    (12, 'Davis', 'Steven', 20, 'M', NULL, 4, 'PIT'),     
    (13, 'Norris', 'Charles', 18, 'M', 5, 24, 'DAL'),     
    (14, 'Lee', 'Susan', 16, 'F', 7, 26, 'HKG'),          
    (15, 'Schwartz', 'Mark', 17, 'M', 6, 20, 'DET'),      
    (16, 'Wilson', 'Bruce', 27, 'M', 8, 1, 'LON'),        
    (17, 'Leighton', 'Michael', 20, 'M', 1, 8, 'PIT'),    
    (18, 'Pang', 'Arthur', 18, 'M', 3, 20, 'WAS'),        
    (19, 'Thornton', 'Ian', 22, 'M', 7, 17, 'NYC'),       
    (20, 'Andreou', 'George', 19, 'M', NULL, 18, 'NYC'),  
    (21, 'Woods', 'Michael', 17, 'M', 4, 14, 'PHL'),      
    (22, 'Shieber', 'David', 20, 'M', 1, 13, 'NYC'),      
    (23, 'Prater', 'Stacy', 18, 'F', 6, 4, 'BAL'),        
    (24, 'Goldman', 'Mark', 18, 'M', 5, 13, 'PIT'),       
    (25, 'Pang', 'Eric', 19, 'M', 8, 19, 'HKG'),          
    (26, 'Brody', 'Paul', 18, 'M', 3, 24, 'LOS'),         
    (27, 'Rugh', 'Eric', 20, 'M', 7, 19, 'ROC'),          
    (28, 'Han', 'Jun', 17, 'M', 2, 6, 'PEK'),             
    (29, 'Cheng', 'Lisa', 21, 'F', 1, 5, 'SFO'),          
    (30, 'Smith', 'Sarah', 20, 'F', 6, 9, 'PHL'),         
    (31, 'Brown', 'Eric', 20, 'M', 5, 12, 'ATL'),         
    (32, 'Simms', 'William', 18, 'M', 3, 12, 'NAR'),      
    (33, 'Epp', 'Eric', 18, 'M', NULL, 23, 'BOS'),        
    (34, 'Schmidt', 'Sarah', 26, 'F', 2, 25, 'WAS')"""),
    'Facility_employee': (
        """INSERT INTO Facility_employee (FacilityID, EmployeeID) VALUES
	(1, 1),   
	(2, 2),   
	(3, 3),   
	(4, 4),   
	(5, 5),   
	(6, 6),   
	(7, 7),   
	(8, 8),   
	(9, 9),   
	(10, 10), 
	(11, 11), 
	(12, 12), 
	(13, 13), 
	(14, 14), 
	(15, 15), 
	(16, 16), 
	(17, 17), 
	(18, 18), 
	(19, 19), 
	(20, 20), 
	(21, 21), 
	(22, 22), 
	(23, 23), 
	(24, 24), 
	(1, 25),  
	(2, 26),  
	(3, 27),  
	(4, 28),  
	(5, 29),  
	(6, 30),  
	(7, 31),  
	(8, 32),  
	(9, 33),  
	(10, 34)""")
}

# Valores para deletar as tabelas
drop = {'Facility_employee': (
    "drop table Facility_employee"),
    'Facility_service': (
        "drop table Facility_service"),
    'Dish': (
        "drop table Dish"),
    'Menu': (
        "drop table Menu"),
    'Employee': (
        "drop table Employee"),
    'Restaurant': (
        "drop table Restaurant"),
    'Role': (
        "drop table Role"),
    'Department': (
        "drop table Department"),
    'Facility': (
        "drop table Facility"),
    'Facility': (
        "drop table Facility"),
    'Service': (
        "drop table Service"),
    'Mountain': (
        "drop table Mountain"),
    'Resort': (
        "drop table Resort")
}

# Valores para teste de update
update = {'Dish': (
    """UPDATE Dish
        SET Dish_Value = 20
        WHERE DishId = 1"""),
    'Employee': (
        """UPDATE Employee
        SET age  = 27
        WHERE Employee.EmployeeId = 5"""),
    'Mountain': (
        """UPDATE Mountain
        SET Number_tracks = 25
        WHERE MoutainId = 14""")
}

# Valores para teste de delete
delete = {'Dish': (
    """DELETE FROM Dish
       WHERE DishId = 12"""),
    'Facility_employee': (
        """DELETE FROM Facility_employee
       WHERE EmployeeID = 16 AND FacilityId = 16"""),
    'Employee': (
        """DELETE FROM Employee
       WHERE EmployeeID = 16""")
}


# Funções
def connect_resgatocao():
    cnx = mysql.connector.connect(host='localhost', database='trabalho_final_db', user='root', password='admin')
    if cnx.is_connected():
        db_info = cnx.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        cursor.close()
    return cnx


def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Deletando {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        select = "select * from " + name
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()


def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuido: ")
        codigo_f = input("Digite a variavel primaria: ")
        codigo = input("Digite o codigo numerico: ")
        query = ['UPDATE ', name, ' SET ', atributo, ' = ', valor, ' WHERE ', codigo_f, '= ', codigo]
        sql = ''.join(query)
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()


def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def update_test(connect):
    print("\n---UPDATE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
            cursor.execute(update_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def delete_test(connect):
    print("\n---DELETE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print("Teste de atualização de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()


def consulta1(connect):
    select_query = """
    SELECT 
    m.Description AS CulinaryType, 
    AVG(R.Rating) AS AverageRestaurantRating,
    AVG(d.Dish_value) AS AverageDishPrice
    FROM 
    Restaurant R,
    Menu m,
    Dish d
    WHERE
    R.RestaurantId = m.RestaurantId and 
    m.MenuId = d.MenuId
    GROUP BY 
    Culinarytype;
    """
    print("Primeira Consulta: Mostrar a media das avaliacoes e dos precos dos restaurantes por tipo de culinaria")
    cursor = connect.cursor()
    cursor.execute(select_query)
    
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)



def consulta2(connect):
    select_query = """
    SELECT 
    r.Resort_name AS ResortName, 
    COUNT(DISTINCT m.MoutainId) AS NumberOfMountains,
    AVG(m.Number_tracks) AS AverageTracksPerMountain,
    COUNT(DISTINCT f.FacilityId) AS NumberOfFacilities
    FROM 
    Mountain m, 
    Resort r, 
    Facility f
    WHERE 
    m.ResortId = r.ResortId
    AND f.ResortId = r.ResortId
    GROUP BY 
    r.Resort_name;
    """
    print("\nSegunda Consulta: Mostrar o numero de montanhas, de estabelecimentos e a media do numero de pistas nas montanhas por resort.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta3(connect):
    select_query = """
    SELECT 
    Department.Description AS DepartmentDescription,
    COUNT(Employee.EmployeeID) AS NumberOfEmployees,
    AVG(Employee.Age) AS AverageEmployeeAge
    FROM 
    Department, Role, Employee
    WHERE 
    Role.DeptId = Department.DeptId
    AND Employee.PosId = Role.PosId
    GROUP BY 
    Department.Description;
    """
    print("\nTerceira Consulta: Mostrar a quantidade de funcionarios e a media de idade dos funcionarios por departamento.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)


def consulta_extra(connect):
    select_query = """
    SELECT facility_employee.FacilityId, facility_employee.EmployeeID, employee.First_name, employee.PosId, role.Job_Title
FROM facility_employee, employee, role
WHERE facility_employee.EmployeeID = employee.EmployeeID
AND employee.PosId = role.PosId
ORDER BY facility_employee.EmployeeID;"""
    print("\nConsulta Extra: Mostrar o estabelecimento, o funcionario e o cargo de todos os empregados.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def plot_consulta1(connect):
    # Consulta SQL
    query = """
SELECT 
    m.Description AS CulinaryType, 
    AVG(R.Rating) AS AverageRestaurantRating,
    AVG(d.Dish_value) AS AverageDishPrice
FROM 
    Restaurant R,
    Menu m,
    Dish d
WHERE
    R.RestaurantId = m.RestaurantId and 
    m.MenuId = d.MenuId
GROUP BY 
    CulinaryType
"""

    # Executar a consulta SQL
    cursor = connect.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Processar os dados para plotagem
    culinary_types = [row[0] for row in results]
    avg_ratings = [row[1] for row in results]
    avg_dish_prices = [row[2] for row in results]
    
    # Passo 3: Plotar o gráfico
    fig, ax1 = plt.subplots()
    
    # Gráfico de barras para a média de preços dos pratos
    color = 'tab:blue'
    ax1.set_xlabel('Culinary Type')
    ax1.set_ylabel('Average Dish Price', color=color)
    ax1.bar(culinary_types, avg_dish_prices, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')
    
    # Gráfico de linha para a média de avaliações dos restaurantes
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Average Restaurant Rating', color=color)
    ax2.plot(culinary_types, avg_ratings, color=color, marker='o')
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()
    plt.title('Average Dish Price and Restaurant Rating by Culinary Type')
    plt.show()

def plot_consulta2(connect):
    # Consulta SQL
    query = """
    SELECT 
    r.Resort_name AS ResortName, 
    COUNT(DISTINCT m.MoutainId) AS NumberOfMountains,
    AVG(m.Number_tracks) AS AverageTracksPerMountain,
    COUNT(DISTINCT f.FacilityId) AS NumberOfFacilities
FROM 
    Mountain m, 
    Resort r, 
    Facility f
WHERE 
    m.ResortId = r.ResortId
    AND f.ResortId = r.ResortId
GROUP BY 
    r.Resort_name
    """

    # Executar a consulta SQL
    cursor = connect.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Processar os dados para plotagem
    resorts = [row[0] for row in results]
    num_mountains = [row[1] for row in results]
    avg_tracks_per_mountain = [row[2] for row in results]
    num_facilities = [row[3] for row in results]
    
    # Passo 3: Plotar o gráfico
    fig, ax1 = plt.subplots()
    
    # Gráfico de barras para o número de montanhas e facilidades
    bar_width = 0.35
    index = np.arange(len(resorts))
    
    bar1 = ax1.bar(index, num_mountains, bar_width, label='Number of Mountains', color='b', alpha=0.6)
    bar2 = ax1.bar(index + bar_width, num_facilities, bar_width, label='Number of Facilities', color='g', alpha=0.6)
    
    ax1.set_xlabel('Resort Name')
    ax1.set_ylabel('Count')
    ax1.set_title('Resorts Analysis')
    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(resorts, rotation=45, ha='right')
    ax1.legend()
    
    # Gráfico de linha para a média de pistas por montanha
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Tracks Per Mountain', color='r')
    ax2.plot(index + bar_width / 2, avg_tracks_per_mountain, color='r', marker='o', label='Average Tracks Per Mountain')
    ax2.tick_params(axis='y', labelcolor='r')
    
    fig.tight_layout()
    plt.title('Number of Mountains, Number of Facilities and Average Tracks per Mountain by Resort')
    plt.show()

def plot_consulta3(connect):
    # Consulta SQL
    query = """
    SELECT 
        Department.Description AS DepartmentDescription,
        COUNT(Employee.EmployeeID) AS NumberOfEmployees,
        AVG(Employee.Age) AS AverageEmployeeAge
    FROM 
        Department, Role, Employee
    WHERE 
        Role.DeptId = Department.DeptId
        AND Employee.PosId = Role.PosId
    GROUP BY 
        Department.Description
    """

    # Executar a consulta SQL
    cursor = connect.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Processar os dados para plotagem
    departments = [row[0] for row in results]
    num_employees = [row[1] for row in results]
    avg_ages = [row[2] for row in results]

    # Plotar o gráfico
    fig, ax1 = plt.subplots()

    # Gráfico de barras para o número de funcionários
    color = 'tab:blue'
    ax1.set_xlabel('Department Description')
    ax1.set_ylabel('Number of Employees', color=color)
    ax1.bar(departments, num_employees, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    # Gráfico de linha para a idade média dos funcionários
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Average Employee Age', color=color)
    ax2.plot(departments, avg_ages, color=color, marker='o')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Number of Employees and Average Employee Age by Department')
    plt.show()

def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão ao MySQL foi encerrada")


def crud_resgatocao(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    #consulta_extra(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    #consulta_extra(connect)


# Main
try:
    # Estabelece Conexão com o DB
    con = connect_resgatocao()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD RESORT MANAGER
        2.  TEST - Create all tables
        3.  TEST - Insert all values
        4.  TEST - Update
        5.  TEST - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  CONSULTA EXTRA
        10. Show Table
        11. Update Value
        12. CLEAR ALL RESORT MANAGER
        13. PLOT CONSULTA 01
        14. PLOT CONSULTA 02
        15. PLOT CONSULTA 03
        0.  Disconnect DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 15:
            print("Erro tente novamente")
            choice = int(input())

        if choice == 0:
            if con.is_connected():
                exit_db(con)
                print("Muito obrigado.")
                break
            else:
                break

        if choice == 1:
            crud_resgatocao(con)

        if choice == 2:
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:
            consulta1(con)

        if choice == 7:
            consulta2(con)

        if choice == 8:
            consulta3(con)

        if choice == 9:
            consulta_extra(con)

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)
        
        if choice == 13:
            plot_consulta1(con)

        if choice == 14:
            plot_consulta2(con)

        if choice == 15:
            plot_consulta3(con)

except mysql.connector.Error as err:
    print("Erro na conexão com o sqlite", err.msg)
