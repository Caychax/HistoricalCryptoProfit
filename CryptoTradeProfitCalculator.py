
# standard imports
import sys
import pyqtgraph
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QSpinBox
from datetime import datetime


class StockTradeProfitCalculator(QDialog):
    '''
    Provides the following functionality:

    - Allows the selection of the stock to be purchased
    - Allows the selection of the quantity to be purchased
    - Allows the selection of the purchase date
    - Displays the purchase total
    - Allows the selection of the sell date
    - Displays the sell total
    - Displays the profit total
    - Additional functionality

    '''

    def __init__(self):

        super().__init__()

        # setting up dictionary of stocks
        self.data = self.make_data()
        # sorting the dictionary of stocks by the keys. The keys at the high level are dates, so we are sorting by date
        self.stocks = sorted(self.data.keys())

        # the following 2 lines of code are for debugging purposee and show you how to access the self.data to get dates and prices
        # print all the dates and close prices for BTC
        # print("all the dates and close prices for BTC", self.data['BTC'])
        # print the close price for BTC on 04/29/2013
        # print("the close price for BTC on 04/29/2013",self.data['BTC'][QDate(2013,4,29)])

        # The data in the file is in the following range
        #  first date in dataset - 29th Apr 2013
        #  last date in dataset - 6th Jul 2021
        # When the calendars load we want to ensure that the default dates selected are within the date range above
        #  we can do this by setting variables to store suitable default values for sellCalendar and buyCalendar.
        self.sellCalendarDefaultDate = sorted(self.data['BTC'].keys())[
            -1]  # Accessing the last element of a python list is explained with method 2 on https://www.geeksforgeeks.org/python-how-to-get-the-last-element-of-list/
        print("self.sellCalendarStartDate", self.sellCalendarDefaultDate)
        self.buyCalendarDefaultDate = sorted(self.data['BTC'].keys())[0]
        print("self.buyCalendarStartDate", self.buyCalendarDefaultDate)
        print(self.data['BTC'][self.buyCalendarDefaultDate])

        # Window Title
        self.setWindowTitle("CryptoTradeProfitCalculator")

        # label for name of app
        self.titleLabel = QLabel("Stock Purchasing app")

        # create QLabel for stock purchased
        self.stockLabel = QLabel(self)
        self.stockLabel.setText("Select a Stock")

        # create QComboBox and populate it with a list of stocks
        self.stockBox = QComboBox(self)
        self.stockBox.addItems(self.stocks)
        self.stockBox.currentTextChanged.connect(self.updateUi)

        # create CalendarWidgets for selection of purchase and sell dates
        # Purchase Calendar Widget
        self.pTitle = QLabel("Purchase Calender")
        self.purchaseCal = QCalendarWidget(self)
        self.purchaseCal.clicked.connect(self.updateUi)
        # Sell Calendar Widget
        self.sTitle = QLabel("Sell Calender")
        self.sellCal = QCalendarWidget(self)
        self.sellCal.clicked.connect(self.updateUi)

        # create QSpinBox to select stock quantity purchased
        self.numStockTitle = QLabel("Amount of stock: ")
        self.numOfStock = QSpinBox()
        self.numOfStock.setRange(1, 1000000)
        self.numOfStock.valueChanged.connect(self.updateUi)

        # create QLabels to show the stock purchase total
        self.purchaseTot = QLabel("Total purchased:")
        self.sellTot = QLabel("Total sold:")

        # create QLabels to show the stock sell total

        # create QLabels to show the stock profit total
        self.profit = QLabel("Profits:")

        # graph section
        self.graphWidget = pyqtgraph.PlotWidget()

        # row 2 - purchase date selection
        self.purchaseCal.setDateRange(sorted(self.data[self.stockBox.currentText()].keys())[0],
                                      sorted(self.data[self.stockBox.currentText()].keys())[-1])
        self.purchaseCal.setSelectedDate(sorted(self.data[self.stockBox.currentText()].keys())[-15])
        # row 3 - display purchase total
        ptot = self.data[self.stockBox.currentText()][self.purchaseCal.selectedDate()] * int(self.numOfStock.text())
        ptxt = "Purchased: " + str("{:.2f}".format(ptot))
        self.purchaseTot.setText(ptxt)
        # row 4 - sell date selection
        # done by default
        # sets boundaries for first stock of list
        self.sellCal.setDateRange(sorted(self.data[self.stockBox.currentText()].keys())[0],
                                  sorted(self.data[self.stockBox.currentText()].keys())[-1])
        # row 5 - display sell total
        stot = self.data[self.stockBox.currentText()][self.sellCal.selectedDate()] * int(self.numOfStock.text())
        stxt = "Sold: " + str("{:.2f}".format(stot))
        self.sellTot.setText(stxt)
        # row 6 - display profit total
        prof = stot - ptot
        prof_text = "Profit: " + "{:.2f}".format(prof) + " $"
        self.profit.setText(prof_text)



        # All form layouts are here:
        # Main layouts
        self.grid = QGridLayout(self)
        self.gridOfOptions = QGridLayout()
        self.grid.addLayout(self.gridOfOptions,1,0)
        self.grid.setHorizontalSpacing(20)

        # Title form
        self.titleLabel.setFont(QFont("Arial", 40))
        self.titleLabel.setContentsMargins(0,20,0,30)
        self.grid.addWidget(self.titleLabel, 0, 0, 1, 2)

        # stock info form
        self.gridOfOptions.addWidget(self.stockBox,0,1)
        self.gridOfOptions.addWidget(self.stockLabel,0,0)

        # stock amount
        self.gridOfOptions.addWidget(self.numStockTitle, 1, 0)
        self.gridOfOptions.addWidget(self.numOfStock, 1, 1)
        self.numOfStock.setFixedSize(100, 30)

        # Purchase calender form
        self.grid.addWidget(self.pTitle, 3, 0)
        self.pTitle.setContentsMargins(0, 30, 0, 10)
        self.grid.addWidget(self.purchaseCal, 4, 0)
        self.grid.addWidget(self.purchaseTot, 5, 0)
        self.purchaseTot.setContentsMargins(0, 20, 0, 0)
        self.purchaseTot.setStyleSheet("font-size: 15px")

        # Sell calendar form
        self.grid.addWidget(self.sTitle, 3, 1)
        self.sTitle.setContentsMargins(0, 30, 0, 10)
        self.grid.addWidget(self.sellCal, 4, 1)
        self.grid.addWidget(self.sellTot, 5, 1)
        self.sellTot.setContentsMargins(0, 20, 0, 0)
        self.sellTot.setStyleSheet("font-size: 15px")

        # Profit form
        self.grid.addWidget(self.profit, 6, 0)
        self.profit.setContentsMargins(0, 20, 0, 20)
        self.profit.setStyleSheet("font-size: 20px")

        # Graph form
        self.graphWidget.setTitle("Stock Closing Prices", color="#666", size="15pt",font="Ariel")
        self.graphWidget.setLabel("left", "Price ($)")
        self.graphWidget.setLabel("bottom", "Time (days)")
        self.grid.addWidget(self.graphWidget,7,0,8,2)


    def stockGraph(self):
        print('')
        # Python is awesome!
        # could not get the date time to be on the axis...
        dev_x = [datetime(d.year(), d.month(), d.day()) for d in self.data[self.stockBox.currentText()].keys()]
        print(dev_x[0])
        dev_y = [float('{:.2f}'.format(v)) for v in self.data[self.stockBox.currentText()].values()]
        print(dev_y[0])
        self.graphWidget.plot(dev_y)

    def updateUi(self):


        try:
            # update calander and labels on stock change
            self.stockLabel.setText("Selected: " + self.stockBox.currentText())
        except Exception as e:
            print("error in stock change update")
        try:
            # current calendar data selected
            pdate = self.purchaseCal.selectedDate()
            sdate = self.sellCal.selectedDate()

            # purchase calendar update
            self.purchaseCal.setDateRange(sorted(self.data[self.stockBox.currentText()].keys())[0],
                                          sorted(self.data[self.stockBox.currentText()].keys())[-1])
            self.purchaseCal.setSelectedDate(sorted(self.data[self.stockBox.currentText()].keys())[-15])
            ptot = self.data[self.stockBox.currentText()][pdate] * int(self.numOfStock.text())
            ptxt = "Purchased: " + str("{:.2f}".format(ptot))
            self.purchaseTot.setText(ptxt)
            print("Purchased: ", ptot)

            # sell calendar update
            # can only sell on a date after the selected purchase date
            self.sellCal.setDateRange(pdate, sorted(self.data[self.stockBox.currentText()].keys())[-1])
            stot = self.data[self.stockBox.currentText()][sdate] * int(self.numOfStock.text())
            stxt = "Sold: " + str("{:.2f}".format(stot))
            self.sellTot.setText(stxt)
            print("Sold:", stot)
            prof = stot - ptot
            prof_text = "Profit: " + "{:.2f}".format(prof)+" $"
            self.profit.setText(prof_text)
            self.stockGraph()
        except KeyError:
            self.purchaseTot.setText("no data")



    def make_data(self):
        '''
        This code is complete
        Data source is derived from https://www.kaggle.com/camnugent/sandp500/download but use the provided file to avoid confusion

        Converts a CSV file to a dictonary fo dictionaries like

            Stock   -> Date      -> Close
            AAL     -> 08/02/2013 -> 14.75
                    -> 11/02/2013 -> 14.46
                    ...
            AAPL    -> 08/02/2013 -> 67.85
                    -> 11/02/2013 -> 65.56


        '''
        file = open("combined.csv",
                    "r")  # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
        data = {}  # empty data dictionary
        file_rows = []  # empty list of file rows
        # add rows to the file_rows list
        for row in file:
            file_rows.append(row.strip())  # https://www.geeksforgeeks.org/python-string-strip-2/
        print("len(file_rows):" + str(len(file_rows)))

        # get the column headings of the CSV file
        row0 = file_rows[0]
        line = row0.split(",")
        column_headings = line
        print(column_headings)

        # get the unique list of stocks from the CSV file
        non_unique_stocks = []
        file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            non_unique_stocks.append(line[6])
        stocks = self.unique(non_unique_stocks)
        print("len(stocks):" + str(len(stocks)))
        print("stocks:" + str(stocks))

        # build the base dictionary of stocks
        for stock in stocks:
            data[stock] = {}

        # build the dictionary of dictionaries
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            date = self.string_date_into_QDate(line[0])
            stock = line[6]
            close_price = line[4]
            # include error handling code if close price is incorrect
            data[stock][date] = float(close_price)
        print("len(data):", len(data))
        return data

    def string_date_into_QDate(self, date_String):
        '''
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        '''
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''
        # intilize a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list


# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    currency_converter = StockTradeProfitCalculator()
    currency_converter.show()
    sys.exit(app.exec_())
