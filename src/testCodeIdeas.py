# dictionary = {"Name":[], "Latitude":[], "Longitude":[], "Cases":[], "Percent":[]}

# dictionary.update({"test": []})

# print(dictionary)

import camelot

def getTable(file):
        #Ask what page to read
        print("What page do you want to read?")
        numOfPages = input()

        tables = camelot.read_pdf(file, pages = str(numOfPages))

        #Print statements
        print("Total Tables Extracted:", tables.n)

        return tables

def findAreaType(location):
        if location == "Country":
                return True
        elif location == "County":
                return True
        elif location == "Territory":
                return True
        elif location == "Region":
                return True
        elif location == "Area":
                return True
        else:
                return False

#PDF file
file = "src\\readingData\\COVID_Data.pdf"

#get the table data
tableData = getTable(file)

foundTable = []  #a list of tables that contain the above cases (represented by index)
foundColumn = []  #a list of columns that contain the above cases (represented by index)
for x in range(tableData.n):
    split = tableData[x].df[0][0]#.split("\n")  #split the first cell by "\n"
    print(split)
    # for y in range(len(split)):
    #     if findAreaType(split[y]):  #if a case matches the table and column are recorded (represented as index)
    #         foundTable.append(x)
    #         foundColumn.append(y)

#tables[x].df[y][z] where 'x' represents which table to look at (if 
#multiple tables were found), 'y' represents the column of the table
#in question, and 'z' represents the row of the table.
#Note: The headers of the table are commonly at index 0. Also the 
#header can sometimes be all in one cell making index 0 of another 
#column be empty.
#Note: len() of the tables[x].df gets the number of rows in a table
#How do you determine the number of columns?

#Convert the table to a csv file
tableData[0].to_csv("test.csv")

#Convert the table to a excel file
    #tables[0].to_excel("test2.xlsx")

print("Enter the State")
state = input()