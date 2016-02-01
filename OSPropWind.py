import FreeCAD, FreeCADGui;
from PySide import QtGui,QtCore;
#from FreeCAD import Base;
App=FreeCAD;
Gui=FreeCADGui;

global OS, Rays;

#------------------------------
def proceedProps():
  #QtGui.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
  # Apply to OSData
  applyProps();
  #QtGui.qApp.restoreOverrideCursor();
  dialog.hide();
#--------------------------
# list for OSData table
cl=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R", \
    "S","T","U","V","W","X","Y","Z"];
#--------------------------
def showProps():
  doc=FreeCAD.ActiveDocument;
  if (hasattr(doc,'OSData')==True):
    osd=doc.OSData;
    # get row count
    RC=int(osd.getContents("B1"));
    RayC=int(osd.getContents("C1"));
    tw.setRowCount(RC);
    # Fill up left header
    L_Str=[];
    i=0;
    while (i<RC):
      L_Str+=[osd.getContents(cl[4]+str(i+1))];
      i=i+1;
    L_Str[0]=osd.getContents(cl[0]+str(1));
    L_Str[1]=osd.getContents(cl[0]+str(2));
    L_Str[RayC-1]=osd.getContents(cl[0]+str(RayC));
    tw.setVerticalHeaderLabels(L_Str);
    tw.setColumnCount(len(cl));
    tw.setHorizontalHeaderLabels(cl);
    # fill up table
    for i in xrange(0,len(cl)):
      for j in xrange(0,RC):
        tw.setItem(j,i, \
          QtGui.QTableWidgetItem(osd.getContents(cl[i]+str(j+1))));
    #FreeCAD.Console.PrintMessage("Row Count is %d\n"%(RC));
  else:
    NR=tw.rowCount();
    if (NR>0): # remove rows for none OSData
      for i in xrange(0,NR):
        tw.removeRow(0);

  dialog.show();
#--------------------------

#--------------------------
def applyProps():
  #FreeCAD.Console.PrintMessage("Props is applyed!\n");
  doc=FreeCAD.ActiveDocument;
  if (hasattr(doc,'OSData')==False):
    doc.addObject('Spreadsheet::Sheet','OSData'); # add Table if no
  osd=doc.OSData;
  RC=tw.rowCount();
  for i in xrange(0,len(cl)):
    for j in xrange(0,RC):
      osd.set(cl[i]+str(j+1),str(tw.item(j,i).text()));
      #FreeCAD.Console.PrintMessage(tw.item(j,i).text()+";");
  doc.recompute();
#--------------------------

#--------------------------
def hideProps():
  dialog.hide();
#--------------------------

#---------------------------
def UpRow():
  row = tw.currentRow();
  column = tw.currentColumn();
  #FreeCAD.Console.PrintMessage("Current row: "+str(row));
  if (row > 1):
    tw.insertRow(row-1);
    for i in range(1,tw.columnCount()):
      tw.setItem(row-1,i,tw.takeItem(row+1,i));
    tw.setItem(row-1,0,tw.takeItem(row,0));
    tw.setItem(row,0,tw.takeItem(row+1,0));
    tw.removeRow(row+1);
    tw.setCurrentCell(row-1,column);
  FreeCAD.Console.PrintMessage("Row is up!\n");
#---------------------------

#---------------------------
def DownRow():
  row = tw.currentRow();
  column = tw.currentColumn();
  #FreeCAD.Console.PrintMessage("Current row: "+str(row));
  if (row < tw.rowCount()-1):
    tw.insertRow(row+2);
    for i in range(1,tw.columnCount()):
      tw.setItem(row+2,i,tw.takeItem(row,i));
    tw.setItem(row+2,0,tw.takeItem(row+1,0));
    tw.setItem(row+1,0,tw.takeItem(row,0));
    tw.removeRow(row);
    tw.setCurrentCell(row+1,column);
  FreeCAD.Console.PrintMessage("Row is down!\n");
#---------------------------

#---------------------------
def CopyRow():
  #osd=FreeCAD.ActiveDocument.OSData;
  FC=int(tw.item(0,1).text()); # full count
  RC=int(tw.item(0,2).text()); # ray count
  row = tw.currentRow();
  #column = tw.currentColumn();
  #FreeCAD.Console.PrintMessage("Current row: "+str(row)+"\n");
  if (row < tw.rowCount()):
    tw.insertRow(row+1);
    FC=FC+1;
    tw.setItem(0,1,QtGui.QTableWidgetItem(str(FC)));
    if (row<RC-2):
      RC=RC+1;
      tw.setItem(0,2,QtGui.QTableWidgetItem(str(RC)));
    str1=[];
    for i in range(0,tw.columnCount()):
      str1+=[tw.item(row,i).text()];
    # coping
    for i in range(0,tw.columnCount()):
      tw.setItem(row+1,i,QtGui.QTableWidgetItem(str1[i]));
    # numbering of optics elements
    for i in range(3,RC-2):
      tw.setItem(i,0,QtGui.QTableWidgetItem(str(i-2)));
    # numbering of rays
    for i in range(RC+1,FC):
      tw.setItem(i,0,QtGui.QTableWidgetItem(str(i-RC)));
    #FreeCAD.Console.PrintMessage(str(str1)+"\n");
  FreeCAD.Console.PrintMessage("Row is copied!\n");
#---------------------------

#---------------------------
def DelRow():
  FC=int(tw.item(0,1).text()); # full count
  RC=int(tw.item(0,2).text()); # ray count
  row = tw.currentRow();
  #column = tw.currentColumn();
  #FreeCAD.Console.PrintMessage("Current row: "+str(row));
  if (row < tw.rowCount()):
    tw.removeRow(row);
    FC=FC-1;
    tw.setItem(0,1,QtGui.QTableWidgetItem(str(FC)));
    if (row<RC-2):
      RC=RC-1;
      tw.setItem(0,2,QtGui.QTableWidgetItem(str(RC)));
    # numbering of optics elements
    for i in range(3,RC-2):
      tw.setItem(i,0,QtGui.QTableWidgetItem(str(i-2)));
    # numbering of rays
    for i in range(RC+1,FC):
      tw.setItem(i,0,QtGui.QTableWidgetItem(str(i-RC)));
  FreeCAD.Console.PrintMessage("Row is deleted!\n");
#---------------------------

#--------------------------- 
dialog = QtGui.QDialog();
dialog.resize(400,400);
dialog.setWindowTitle("Properties of optical system");
la = QtGui.QVBoxLayout(dialog);
 
e1 = QtGui.QLabel("Properties");
commentFont=QtGui.QFont("Arial",8,True);
e1.setFont(commentFont);
la.addWidget(e1);
 
# Create table
tw = QtGui.QTableWidget();
tw.setColumnCount(1);
Header=["Value"];
tw.setHorizontalHeaderLabels(Header);
#it=tw.item(1,1).text();
#FreeCAD.Console.PrintMessage(it);
la.addWidget(tw);

# rule buttons for table rows
UpBtn = QtGui.QPushButton("Up");
DownBtn = QtGui.QPushButton("Down");
CopyBtn = QtGui.QPushButton("Copy");
DelBtn = QtGui.QPushButton("Delete");
buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);
buttonBox.addButton(UpBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox.addButton(DownBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox.addButton(CopyBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox.addButton(DelBtn, QtGui.QDialogButtonBox.ActionRole)
la.addWidget(buttonBox);

OkBtn = QtGui.QPushButton("Ok");
ApplyBtn = QtGui.QPushButton("Apply");
CancelBtn = QtGui.QPushButton("Cancel");
buttonBox2 = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);
buttonBox2.addButton(OkBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox2.addButton(ApplyBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox2.addButton(CancelBtn, QtGui.QDialogButtonBox.ActionRole)
la.addWidget(buttonBox2);

QtCore.QObject.connect(UpBtn, QtCore.SIGNAL("clicked()"), UpRow);
QtCore.QObject.connect(DownBtn, QtCore.SIGNAL("clicked()"), DownRow);
QtCore.QObject.connect(CopyBtn, QtCore.SIGNAL("clicked()"), CopyRow);
QtCore.QObject.connect(DelBtn, QtCore.SIGNAL("clicked()"), DelRow);
QtCore.QObject.connect(OkBtn, QtCore.SIGNAL("clicked()"), proceedProps);
QtCore.QObject.connect(ApplyBtn, QtCore.SIGNAL("clicked()"), applyProps);
QtCore.QObject.connect(CancelBtn, QtCore.SIGNAL("clicked()"), hideProps);

QtCore.QMetaObject.connectSlotsByName(dialog);
#---------------------------