import FreeCAD, FreeCADGui, ImportGui;
import OptElementsGui, Draft, math;
from PySide import QtGui, QtCore;

#--------------------------
def showBuilder():
  changeTable();
  dialog.show();
# end def
#--------------------------

#------------------------------
def proceed():
  if (combo1.currentText()=='Lens'):
    CreateBulkLens();
  # end if
  if (combo1.currentText()=='Plate'):
    CreateBulkPlate();
  # end if    
  if (combo1.currentText()=='Prism'):
    CreateBulkPrism();
  # end if
  if (combo1.currentText()=='Import from ...'):
    ImportElement();
  # end if
  dialog.hide();
# end def
#--------------------------

#--------------------------
def cancel():
  dialog.hide();
# end def
#--------------------------

#--------------------------
def changeTable():
  if (combo1.currentText()=='Lens'):
    str1=['Label','Aperture, mm','Radius R1, mm','Radius R2, mm', \
      'Thickness R1,R2, mm','RI'];
    tw.setRowCount(len(str1));
    tw.setVerticalHeaderLabels(str1);
    tw.setItem(0,0,QtGui.QTableWidgetItem(str('BLEN')));
    tw.setItem(0,1,QtGui.QTableWidgetItem(str(25.5)));
    tw.setItem(0,2,QtGui.QTableWidgetItem(str(24.)));
    tw.setItem(0,3,QtGui.QTableWidgetItem(str(-134.6)));
    tw.setItem(0,4,QtGui.QTableWidgetItem(str(6.5)));
    tw.setItem(0,5,QtGui.QTableWidgetItem(str(1.52)));
  # end if
  if (combo1.currentText()=='Plate'):
    str1=['Label','Width, mm','Height, mm','Thickness, mm','RI'];
    tw.setRowCount(len(str1));
    tw.setVerticalHeaderLabels(str1);
    tw.setItem(0,0,QtGui.QTableWidgetItem(str('BPLT')));
    tw.setItem(0,1,QtGui.QTableWidgetItem(str(25.5)));
    tw.setItem(0,2,QtGui.QTableWidgetItem(str(25.5)));
    tw.setItem(0,3,QtGui.QTableWidgetItem(str(5.)));
    tw.setItem(0,4,QtGui.QTableWidgetItem(str(1.52)));
  # end if
  if (combo1.currentText()=='Prism'):
    str1=['Label','Length side 1, mm','Length side 2, mm','Angle, degrees', \
      'Thickness, mm','RI'];
    tw.setRowCount(len(str1));
    tw.setVerticalHeaderLabels(str1);
    tw.setItem(0,0,QtGui.QTableWidgetItem(str('BPRISM')));
    tw.setItem(0,1,QtGui.QTableWidgetItem(str(25.5)));
    tw.setItem(0,2,QtGui.QTableWidgetItem(str(25.5)));
    tw.setItem(0,3,QtGui.QTableWidgetItem(str(90.)));
    tw.setItem(0,4,QtGui.QTableWidgetItem(str(25.5)));
    tw.setItem(0,5,QtGui.QTableWidgetItem(str(1.52)));
  # end if
  if (combo1.currentText()=='Import from ...'):
    str1=['Load from file'];
    tw.setRowCount(len(str1));
    tw.setItem(0,0,QtGui.QTableWidgetItem(str('...')));    
    tw.setVerticalHeaderLabels(str1);
  # end if
# end def
#--------------------------

#--------------------------
def ImportElement():
  doc=FreeCAD.ActiveDocument;
  FreeCAD.Console.PrintMessage("Try to import...\n");
  (fname1,fdir1) = QtGui.QFileDialog.getOpenFileName(None,'Open file','');
  ImportGui.insert(fname1,doc.Name);
  doc.recompute();
  ob1=doc.Objects[-1];
    # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(ob1);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(ob1);
  # end if
  ob1.Label="IMPR";
  ob1.ViewObject.ShapeColor=(0.5,0.5,0.5);
  ob1.ViewObject.Transparency=80;
  An=ob1.Placement.Rotation.toEuler();
  P1=ob1.Placement.Base;
  l1=["","Imported",ob1.Name,ob1.Label, \
      P1.x,P1.y,P1.z, \
      An[2],An[1],An[0],None,None,None,1.,1.52,None,None];
  # add lens to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  doc.recompute();
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  FreeCAD.Console.PrintMessage("Element is imported\n");
# end def
#--------------------------

#--------------------------
def CreateInterface():
  doc=FreeCAD.ActiveDocument;
  l=25.5; h=25.5;
  pl = FreeCAD.Placement();
  pl.Rotation = FreeCAD.Rotation(0.,0.,0.);
  pl.Base = FreeCAD.Vector(-l/2.,-h/2.,0.);
  int_ob=Draft.makeRectangle(length=l,height=h,placement=pl,face=False, \
                             support=None);
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(int_ob);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(int_ob);
  # end if
  int_ob.MakeFace = True;
  int_ob.Label="INT";
  int_ob.ViewObject.ShapeColor=(0.5,0.5,0.5);
  int_ob.ViewObject.Transparency=80;
  An=pl.Rotation.toEuler();
  l1=["","Interface",int_ob.Name,int_ob.Label, \
      pl.Base.x+l/2.,pl.Base.y+h/2.,pl.Base.z, \
      An[2],An[1],An[0],None,l,h,1.,1.,None,None];
  # add lens to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  doc.recompute();
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  FreeCAD.Console.PrintMessage("Intefrace was created\n");
# end def
#--------------------------

#--------------------------
def CreatePlate():
  doc=FreeCAD.ActiveDocument;
  l=25.5; h=25.5;
  pl = FreeCAD.Placement();
  pl.Rotation = FreeCAD.Rotation(0.,0.,0.);
  pl.Base = FreeCAD.Vector(-l/2.,-h/2.,0.);
  # First interface
  int_ob1=Draft.makeRectangle(length=l,height=h,placement=pl,face=False, \
                              support=None);
  int_ob1.MakeFace = True;
  int_ob1.Label="PLT1";
  int_ob1.ViewObject.ShapeColor=(0.5,0.5,0.5);
  # Second interface 1 mm thickness
  pl.Base = FreeCAD.Vector(-l/2.,-h/2.,1.);
  int_ob2=Draft.makeRectangle(length=l,height=h,placement=pl,face=False, \
                              support=None);
  int_ob2.MakeFace = True;
  int_ob2.Label="PLT2";
  int_ob2.ViewObject.ShapeColor=(0.5,0.5,0.5);
  # Add to Fusion Plate
  # Create Fusion
  plt_ob=doc.addObject("Part::MultiFuse","IPLT");
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(plt_ob);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(plt_ob);
  # end if
  plt_ob.Shapes = [int_ob1,int_ob2];
  int_ob1.ViewObject.Visibility=False;
  int_ob2.ViewObject.Visibility=False;
  plt_ob.ViewObject.ShapeColor=int_ob1.ViewObject.ShapeColor;
  plt_ob.ViewObject.Transparency=80;
  doc.recompute();
  t1=(plt_ob.Shape.Faces[0].Placement.Base- \
    plt_ob.Shape.Faces[1].Placement.Base).Length;
  An=pl.Rotation.toEuler();
  l1=["","IPlate",plt_ob.Name,plt_ob.Label, \
      pl.Base.x+l/2.,pl.Base.y+h/2.,pl.Base.z, \
      An[2],An[1],An[0],None,l,h,1.,1.,None,t1];
  # add plate to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  FreeCAD.Console.PrintMessage("Plate was created\n");
# end def
#--------------------------

#--------------------------
def CreateScreen():
  doc=FreeCAD.ActiveDocument;
  l=25.5; h=25.5;
  pl = FreeCAD.Placement();
  pl.Rotation = FreeCAD.Rotation(0.,0.,0.);
  pl.Base = FreeCAD.Vector(-l/2.,-h/2.,0.);
  scr_ob=Draft.makeRectangle(length=l,height=h,placement=pl,face=False, \
                             support=None);
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(scr_ob);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(scr_ob);
  # end if
  scr_ob.MakeFace = True;
  scr_ob.Label="SCR";
  scr_ob.ViewObject.ShapeColor=(0.5,0.5,0.5);
  An=pl.Rotation.toEuler();
  l1=["","Screen",scr_ob.Name,scr_ob.Label, \
      pl.Base.x+l/2.,pl.Base.y+h/2.,pl.Base.z, \
      An[2],An[1],An[0],None,l,h,1.,1.,None,None];
  OptElementsGui.AddToOSData(l1,"Element"); # add lens to list of optical system elements    
  doc.recompute();
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  FreeCAD.Console.PrintMessage("Screen was created\n");
# end def
#--------------------------

#--------------------------
def CreateMirror():
  doc=FreeCAD.ActiveDocument;
  mirr_ob=Draft.makeCircle(10);
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(mirr_ob);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(mirr_ob);
  # end if
  mirr_ob.MakeFace=True;
  mirr_ob.Label="MIR";
  mirr_ob.Radius.Value=25.5/2.;
  mirr_ob.ViewObject.ShapeColor=(1.,1.,1.);
  R=mirr_ob.Placement.Base;
  An=mirr_ob.Placement.Rotation.toEuler();
  Ap=2.*mirr_ob.Radius.Value;
  l1=["","Mirror",mirr_ob.Name,mirr_ob.Label,R.x,R.y,R.z,An[2],An[1],An[0], \
    Ap,None,None,None,None,None,None];
  # add mirror to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  doc.recompute();
  FreeCAD.Console.PrintMessage("Mirror was created\n");
# end def
#--------------------------

#--------------------------
def CreateLens():
  doc=FreeCAD.ActiveDocument;
  lens_ob=Draft.makeCircle(10);
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(lens_ob);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(lens_ob);
  # end if
  lens_ob.MakeFace=True;
  lens_ob.Label="PLEN";
  lens_ob.Radius.Value=25.5/2.;
  lens_ob.ViewObject.ShapeColor=(0.5,0.5,0.5);
  lens_ob.ViewObject.Transparency=60;
  R=lens_ob.Placement.Base;
  An=lens_ob.Placement.Rotation.toEuler();
  Ap=2.*lens_ob.Radius.Value;
  f=0.1*1000.;
  l1=["","ThinLens",lens_ob.Name,lens_ob.Label,R.x,R.y,R.z, \
      An[2],An[1],An[0],Ap,None,None,None,None,f,None];
  OptElementsGui.AddToOSData(l1,"Element"); # add lens to list of optical system elements
  doc.recompute();
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  doc.recompute();
  FreeCAD.Console.PrintMessage("Lens was created\n");
#end def
#--------------------------

#--------------------------
def CreateInitialRay():
  doc=FreeCAD.ActiveDocument;
  ray_ob=doc.addObject("Part::Line","IR");
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1_r=gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_r.addObject(ray_ob);
  else:
    gr1_r=getattr(doc,'Rays');
    gr1_r.addObject(ray_ob);
  # end if
  ray_ob.X1=0.; ray_ob.Y1=0.; ray_ob.Z1=0.;
  ray_ob.X2=0.; ray_ob.Y2=0.; ray_ob.Z2=1.;
  ray_ob.ViewObject.LineWidth=1.;
  Pr=FreeCAD.Vector(0.,0.,0.);
  ray_ob.Placement.Base=Pr;
  An=ray_ob.Placement.Rotation.toEuler();
  wl1=555.;
  col1=ray_ob.ViewObject.LineColor;
  length1=ray_ob.Shape.Length;
  l1=["","Ray",ray_ob.Name,ray_ob.Label, Pr[0], Pr[1], Pr[2], \
      An[2], An[1], An[0], wl1, str(col1), length1];
  OptElementsGui.AddToOSData(l1,"Ray");
  doc.recompute();
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  FreeCAD.Console.PrintMessage("Initial Ray was created\n");
# end def
#--------------------------

#--------------------------
def CreateBulkLens():
  OptElementsGui.CreateData("");
  OptElementsGui.UpdateFunction();
  doc=FreeCAD.ActiveDocument;
  A1=float(tw.item(0,1).text()); # aperture
  R1=float(tw.item(0,2).text()); # radius 1
  R2=float(tw.item(0,3).text()); # radius 2
  T1=float(tw.item(0,4).text()); # thickness
  n1=1.;
  n2=float(tw.item(0,5).text()); # refractive index
  if ((abs(R1)!=float("inf")) and (abs(R2)!=float("inf"))):
    # First object
    ob1=doc.addObject("Part::Cylinder","BLC1");
    ob1.Radius=A1/2.;
    ob1.Height=abs(R1)+abs(R2)+abs(T1);
    ob1.Placement.Base=FreeCAD.Vector(0.,0.,-abs(R1));
    # First sphere
    ob2=doc.addObject("Part::Sphere","BLS1");
    ob2.Radius=abs(R1);
    ob2.Placement.Base=FreeCAD.Vector(0.,0.,R1);
    if (R1>0):
      # First common
      ob3=doc.addObject("Part::MultiCommon","CS1");
      ob3.Shapes=[ob1,ob2];
      ob1.ViewObject.Visibility=False;
      ob2.ViewObject.Visibility=False;
      doc.recompute();  
    else:
      # First cut
      ob3=doc.addObject("Part::Cut","CS1");
      ob3.Base=ob1;
      ob3.Tool=ob2;    
      ob1.ViewObject.Visibility=False;
      ob2.ViewObject.Visibility=False;
      doc.recompute();
    # end if
    # Second sphere
    ob4=doc.addObject("Part::Sphere","BLS2");
    ob4.Radius=abs(R2);
    ob4.Placement.Base=FreeCAD.Vector(0.,0.,R2+T1);
    if (R2>0):
      # Last cut
      blen_ob=doc.addObject("Part::Cut","BLEN");
      blen_ob.Base=ob3;
      blen_ob.Tool=ob4;    
      ob3.ViewObject.Visibility=False;
      ob4.ViewObject.Visibility=False;
      doc.recompute();    
    else:
      # Last common
      blen_ob=doc.addObject("Part::MultiCommon","BLEN");
      blen_ob.Shapes=[ob3,ob4];
      ob3.ViewObject.Visibility=False;
      ob4.ViewObject.Visibility=False;
      doc.recompute();
    # end if
  elif ((abs(R1)==float("inf")) and (abs(R2)!=float("inf"))):
    # First object of plane-spherical lens
    ob1=doc.addObject("Part::Cylinder","BLC1");
    ob1.Radius=A1/2.;
    ob1.Height=abs(R2)+abs(T1);
    ob1.Placement.Base=FreeCAD.Vector(0.,0.,0.);
    # Second sphere
    ob4=doc.addObject("Part::Sphere","BLS2");
    ob4.Radius=abs(R2);
    ob4.Placement.Base=FreeCAD.Vector(0.,0.,R2+T1);
    if (R2>0):
      # Last cut
      blen_ob=doc.addObject("Part::Cut","BLEN");
      blen_ob.Base=ob1;
      blen_ob.Tool=ob4;    
      ob1.ViewObject.Visibility=False;
      ob4.ViewObject.Visibility=False;
      doc.recompute();    
    else:
      # Last common
      blen_ob=doc.addObject("Part::MultiCommon","BLEN");
      blen_ob.Shapes=[ob1,ob4];
      ob1.ViewObject.Visibility=False;
      ob4.ViewObject.Visibility=False;
      doc.recompute();
    # end if
  elif ((abs(R1)!=float("inf")) and (abs(R2)==float("inf"))):
    # First object of spherical-plane lens
    # First object
    ob1=doc.addObject("Part::Cylinder","BLC1");
    ob1.Radius=A1/2.;
    ob1.Height=abs(R1)+abs(T1);
    ob1.Placement.Base=FreeCAD.Vector(0.,0.,-abs(R1));
    # First sphere
    ob2=doc.addObject("Part::Sphere","BLS1");
    ob2.Radius=abs(R1);
    ob2.Placement.Base=FreeCAD.Vector(0.,0.,R1);
    if (R1>0):
      # First common
      blen_ob=doc.addObject("Part::MultiCommon","BLEN");
      blen_ob.Shapes=[ob1,ob2];
      ob1.ViewObject.Visibility=False;
      ob2.ViewObject.Visibility=False;
      doc.recompute();  
    else:
      # First cut
      blen_ob=doc.addObject("Part::Cut","BLEN");
      blen_ob.Base=ob1;
      blen_ob.Tool=ob2; 
      ob1.ViewObject.Visibility=False;
      ob2.ViewObject.Visibility=False;
      doc.recompute();
    # end if
  # end if  
  blen_ob.ViewObject.ShapeColor=(0.5,0.5,0.5);
  blen_ob.ViewObject.DisplayMode='Flat Lines';
  blen_ob.ViewObject.Transparency=60;
  P1=blen_ob.Placement.Base;
  An=blen_ob.Placement.Rotation.toEuler();
  doc.recompute();
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(blen_ob);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(blen_ob);
  # end if
  l1=["","BulkLens",blen_ob.Name,blen_ob.Label,P1.x,P1.y,P1.z, \
      An[2],An[1],An[0],A1,None,None,n1,n2,None,T1];
  # Add lens to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  doc.recompute();
  FreeCAD.Console.PrintMessage("Bulk Lens was created\n");

def CreateBulkPlate():
  OptElementsGui.CreateData("");
  OptElementsGui.UpdateFunction();
  doc=FreeCAD.ActiveDocument;
  W1=float(tw.item(0,1).text()); # width
  H1=float(tw.item(0,2).text()); # height
  T1=float(tw.item(0,3).text()); # thickness
  n1=1.;
  n2=float(tw.item(0,4).text()); # refractive index
  #ob1=doc.addObject("Part::Box","Box");
  ob1=doc.addObject("Part::Wedge","Wedge");
  ob1.Xmin=-W1/2.; ob1.Xmax=W1/2.; ob1.X2min=-W1/2.; ob1.X2max=W1/2.;
  ob1.Ymin=-H1/2.; ob1.Ymax=H1/2.;
  ob1.Zmin=-T1/2.; ob1.Zmax=T1/2.; ob1.Z2min=-T1/2.; ob1.Z2max=T1/2.;
  ob1.Label="BPLT";
  doc.recompute();
  #ob1.Length.Value=W1;
  #ob1.Width.Value=H1;
  #ob1.Height.Value=T1;
  #ob1.Placement.Base=FreeCAD.Vector(-W1/2.,-H1/2.,0.);
  ob1.ViewObject.ShapeColor=(0.5,0.5,0.5);
  ob1.ViewObject.DisplayMode='Flat Lines';
  ob1.ViewObject.Transparency=60;
  doc.recompute();
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(ob1);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(ob1);
  # end if
  P1=ob1.Placement.Base;
  An=ob1.Placement.Rotation.toEuler();
  l1=["","BulkPlate",ob1.Name,ob1.Label,P1.x,P1.y,P1.z, \
      An[2],An[1],An[0],None,W1,H1,n1,n2,None,T1];
  # Add plate to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  doc.recompute();
  FreeCAD.Console.PrintMessage("Bulk plate was created\n");
# end def

def CreateBulkPrism():
  OptElementsGui.CreateData("");
  OptElementsGui.UpdateFunction();
  doc=FreeCAD.ActiveDocument;
  LS1=float(tw.item(0,1).text()); # Length of side 1, mm
  LS2=float(tw.item(0,2).text()); # Length of side 2, mm
  AP1=float(tw.item(0,3).text()); # Angle, degrees
  T1=float(tw.item(0,4).text()); # Thickness
  n1=1.;
  n2=float(tw.item(0,5).text()); # refractive index
  ob1=doc.addObject("Part::Wedge","Wedge");
  LS3=(LS1**2.+LS2**2.-2.*LS1*LS2*math.cos(math.pi*AP1/180.))**0.5;
  X1=(LS3**2.+LS1**2.-LS2**2.)/(2.*LS3);
  H1=(LS1**2.-X1**2.)**0.5;
  # Width
  ob1.Xmin.Value=-T1/2.; ob1.Xmax.Value=T1/2.;
  ob1.X2min.Value=-T1/2.; ob1.X2max.Value=T1/2.;
  # Height
  ob1.Zmin.Value=-LS3/2.; ob1.Zmax.Value=LS3/2.;
  ob1.Z2min.Value=0.; ob1.Z2max.Value=0.;
  # Thickness
  ob1.Ymin.Value=0.; ob1.Ymax.Value=H1;
  ob1.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,0), \
    FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-90));
  ob1.Label="BPRISM";
  doc.recompute();
  ob1.ViewObject.ShapeColor=(0.5,0.5,0.5);
  ob1.ViewObject.DisplayMode='Flat Lines';
  ob1.ViewObject.Transparency=60;
  doc.recompute();
  # create groupe and add element to it
  if (hasattr(doc,'OpticalSystem')==False):
    gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
    gr1.newObject("App::DocumentObjectGroup","Rays");
    gr1_e=gr1.newObject("App::DocumentObjectGroup","Elements");
    gr1_e.addObject(ob1);
  else:
    gr1_e=getattr(doc,'Elements');
    gr1_e.addObject(ob1);
  # end if
  P1=ob1.Placement.Base;
  An=ob1.Placement.Rotation.toEuler();
  l1=["","BulkPrism",ob1.Name,ob1.Label,P1.x,P1.y,P1.z, \
      An[2],An[1],An[0],None,LS3,H1,n1,n2,None,T1];
  # Add plate to list of optical system elements
  OptElementsGui.AddToOSData(l1,"Element");
  if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
    FreeCADGui.activeDocument().activeView().viewRear();
    FreeCADGui.activeDocument().activeView().viewRotateRight();
    FreeCADGui.activeDocument().activeView().fitAll();
  # end if
  doc.recompute();
  FreeCAD.Console.PrintMessage("Bulk prism is created\n");
# end def

#--------------------------- 
dialog = QtGui.QDialog();
dialog.resize(250,400);
dialog.setWindowTitle("Optical elements builder");
la = QtGui.QVBoxLayout(dialog);
 
# Create combobox
combo1 = QtGui.QComboBox();
la.addWidget(combo1);
combo1_list=['Lens','Plate','Prism','Import from ...'];
combo1.addItems(combo1_list);

# Create table
tw = QtGui.QTableWidget();
tw.setColumnCount(1);
Header=["Value"];
tw.setHorizontalHeaderLabels(Header);
la.addWidget(tw);

OkBtn = QtGui.QPushButton("Ok");
CancelBtn = QtGui.QPushButton("Cancel");
buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal);
buttonBox.addButton(OkBtn, QtGui.QDialogButtonBox.ActionRole)
buttonBox.addButton(CancelBtn, QtGui.QDialogButtonBox.ActionRole)
la.addWidget(buttonBox);

QtCore.QObject.connect(OkBtn, QtCore.SIGNAL("clicked()"), proceed);
QtCore.QObject.connect(CancelBtn, QtCore.SIGNAL("clicked()"), cancel);
QtCore.QObject.connect(combo1,QtCore.SIGNAL('activated(QString)'),changeTable);

QtCore.QMetaObject.connectSlotsByName(dialog);
#---------------------------