import FreeCAD, FreeCADGui;
from PySide import QtGui,QtCore;
App=FreeCAD;
Gui=FreeCADGui;

#------------------------------
def proceedProps():
  QtGui.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)
  applyProps();
  App.ActiveDocument.recompute();
  QtGui.qApp.restoreOverrideCursor();
  dialog.hide();
# end def
#--------------------------
# list for OSData table
cl=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R", \
    "S","T","U","V","W","X","Y","Z"];
#--------------------------
def showProps():
  SL=Gui.Selection.getSelection();
  if (SL!=[]):
    doc=FreeCAD.ActiveDocument;
    osd=doc.OSData;
    # get full count
    FC=int(osd.getContents("B1"));
    # get ray count    
    RC=int(osd.getContents("C1"));
    EC=0; # element count
    for i in xrange(4,FC+1):
      if (osd.getContents("D"+str(i))==SL[0].Name):
        EC=i;
        break;
      # end if
    # end for i
    if (EC==0):
      NR=tw.rowCount();
      if (NR>0): # remove rows for no selection case
        for i in xrange(0,NR):
          tw.removeRow(0);
        # end for i
      # end if
    # end if
    L_Str=[];
    L_Data=[];
    for i in xrange(len(cl)):
      if ((SL[0].Name).find("IR")==-1):
        # loading of property in cc variable
        cc=osd.getContents(cl[i]+str(3));
      else:
        cc=osd.getContents(cl[i]+str(RC+1));
      if (cc!=""):
        L_Str+=[cc];
        L_Data+=[osd.getContents(cl[i]+str(EC))];
      # end if
    # end for i
    NPL=len(L_Str); # number of rows
    tw.setRowCount(NPL);
    tw.setVerticalHeaderLabels(L_Str);
    for i in xrange(0,NPL):
      tw.setItem(0,i,QtGui.QTableWidgetItem(str(L_Data[i])));
    # end for i
  else:
    NR=tw.rowCount();
    if (NR>0): # remove rows for no selection case
      for i in xrange(0,NR):
        tw.removeRow(0);
      # end for i
    # end if
  # end if
  dialog.show();
# end def
#--------------------------

#--------------------------
def applyProps():
  NR=tw.rowCount();
  if (NR!=0):
    doc=FreeCAD.ActiveDocument;
    if (hasattr(doc,'OSData')==False):
      doc.addObject('Spreadsheet::Sheet','OSData'); # add Table if no
    # end if
    osd=doc.OSData;
    Num1=int(tw.item(0,0).text());
    for i in xrange(0,NR):
      if (str(tw.item(0,2).text())!='Ray'):
        osd.set(cl[i]+str(3+Num1),str(tw.item(0,i).text()));
      else:
        RC=int(osd.getContents("C1"));
        osd.set(cl[i]+str(RC+1+Num1),str(tw.item(0,i).text()));
      "end if"
    "end for i"
    doc.recompute();
  # end if
  FreeCAD.Console.PrintMessage("Props is applyed!\n");
# end def
#--------------------------

#--------------------------
def hideProps():
  dialog.hide();
# end def
#--------------------------

#--------------------------- 
dialog = QtGui.QDialog();
dialog.resize(280,400);
dialog.setWindowTitle("Properties of optical element");
la = QtGui.QVBoxLayout(dialog);
 
e1 = QtGui.QLabel("Properties");
commentFont=QtGui.QFont("Arial",10,True);
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

OkBtn = QtGui.QPushButton("Ok");
ApplyBtn = QtGui.QPushButton("Apply");
CancelBtn = QtGui.QPushButton("Cancel");
buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);
buttonBox.addButton(OkBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox.addButton(ApplyBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox.addButton(CancelBtn, QtGui.QDialogButtonBox.ActionRole)
la.addWidget(buttonBox);

QtCore.QObject.connect(OkBtn, QtCore.SIGNAL("clicked()"), proceedProps);
QtCore.QObject.connect(ApplyBtn, QtCore.SIGNAL("clicked()"), applyProps);
QtCore.QObject.connect(CancelBtn, QtCore.SIGNAL("clicked()"), hideProps);

QtCore.QMetaObject.connectSlotsByName(dialog);
#---------------------------