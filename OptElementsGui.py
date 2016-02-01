import FreeCAD, FreeCADGui;
import OSPropWind, ElemsPropWind, ElemsBuilder, CalcRays;

#--------------------------------------------------
class OrientZXFitAllTool:
  """Rays tool object"""
  def GetResources(self):
    return {"MenuText": "OrZXAll",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Orientation ZX and Fit All"};
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
#    doc=FreeCAD.ActiveDocument;
    if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
      FreeCADGui.activeDocument().activeView().viewRear();
      FreeCADGui.activeDocument().activeView().viewRotateRight();
      FreeCADGui.activeDocument().activeView().fitAll();
    # end if
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('SetOrientZXFitAll',OrientZXFitAllTool());

#--------------------------------------------------
class OrientZXTool:
  """Rays tool object"""
  def GetResources(self):
    return {"MenuText": "OrZX",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Orientation ZX"};
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
#    doc=FreeCAD.ActiveDocument;
    if (str(FreeCADGui.ActiveDocument.activeView())=='View3DInventor'):
      FreeCADGui.activeDocument().activeView().viewRear();
      FreeCADGui.activeDocument().activeView().viewRotateRight();
    # end if
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('SetOrientZX',OrientZXTool());

#------------------------------------------------------
class OSPropTool:
  """Properties tool of optical object"""
  def GetResources(self):
    return {"MenuText": "OSPr",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Properties of optical system"};
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    # start properties window
    OSPropWind.showProps();
  # end def
# end class
#----------------------------

FreeCADGui.addCommand('OSPropTool',OSPropTool());

#------------------------------------------------------
class ElPropTool:
  """Properties tool of optical object"""
  def GetResources(self):
    return {"MenuText": "ElPr",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Properties of object"};
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    # start properties window
    ElemsPropWind.showProps();
  # end def
# end class
#----------------------------

FreeCADGui.addCommand('ElPropTool',ElPropTool());

#------------------------------------------------------
class ElBuildTool:
  """Properties tool of optical object"""
  def GetResources(self):
    return {"MenuText": "ElBuilder",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Optical elements builder"};
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    # start properties window
    ElemsBuilder.showBuilder();
  # end def
#----------------------------

FreeCADGui.addCommand('ElBuildTool',ElBuildTool());

#--------------------------------------------------
class RaysTool:
  """Rays tool object"""
  def GetResources(self):
    return {"MenuText": "RAY",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Create Ray"}; #,
  # end def
#	    "Pixmap": """
#		      /* XPM */
#		      static const char *test_icon[]={
#		      "16 16 2 1",
#		      "a c #000000",
#		      ". c None",
#		      "................",
#		      "................",
#		      "..############..",
#		      "..############..",
#		      "..##........##..",
#		      "..##........##..",
#		      "..##........##..",
#		      "..############..",
#		      "..############..",
#		      "..##....##......",
#		      "..##.....##.....",
#		      "..##......##....",
#		      "..##.......##...",
#		      "..##........##..",
#		      "................",
#		      "................"};
#		      """};
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    CreateData("RayData");    
    UpdateFunction();
    ElemsBuilder.CreateInitialRay();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('CreateRay',RaysTool());

#--------------------------------------------------
class LensTool:
  """Lens tool object"""
  def GetResources(self):
    return {"MenuText": "PLENS",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Create paraxial lens"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    CreateData("");
    UpdateFunction();
    ElemsBuilder.CreateLens();
  # end
# end class
#---------------------------

FreeCADGui.addCommand('CreateLens',LensTool());

#--------------------------------------------------
class MirrorTool:
  """Mirror tool object"""
  def GetResources(self):
    return {"MenuText": "MIRR",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Create Mirror"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  def Activated(self):
    CreateData("");
    UpdateFunction();
    ElemsBuilder.CreateMirror();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('CreateMirror',MirrorTool());

#--------------------------------------------------
class ScreenTool:
  """Screen tool object"""
  def GetResources(self):
    return {"MenuText": "SCR",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Create Screen"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  def Activated(self):
    CreateData("");
    UpdateFunction();
    ElemsBuilder.CreateScreen();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('CreateScreen',ScreenTool());

#--------------------------------------------------
class InterfaceTool:
  """Screen tool object"""
  def GetResources(self):
    return {"MenuText": "INT",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Create Interface"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    CreateData("");
    UpdateFunction();
    ElemsBuilder.CreateInterface();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('CreateInterface',InterfaceTool());

#--------------------------------------------------
class PlateTool:
  """Screen tool object"""
  def GetResources(self):
    return {"MenuText": "IPLT",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Create plate on two interfaces"};
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    CreateData("");
    UpdateFunction();
    ElemsBuilder.CreatePlate();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('CreatePlate',PlateTool());

#--------------------------------------------------
class UpdateTool:
  """Update tool"""
  def GetResources(self):
    return {"MenuText": "Upt",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Update OS to apply changes"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    CreateData("");
    UpdateFunction();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('UpdateOS',UpdateTool());

#---------------------------

#--------------------------------------------------
class CalcTool:
  """Screen tool object"""
  def GetResources(self):
    return {"MenuText": "CalcRP",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Calculate ray propagation"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  def Activated(self):
    # Update state of the optical system
    CreateData("");
    UpdateFunction();
    # Start calculation
    CalcRays.CalculateFunction();
  # end def
# end class
#---------------------------

FreeCADGui.addCommand('CalculateRayPropag',CalcTool());

#---------------------------
class MouseTool:
  """Screen tool object"""
  def GetResources(self):
    return {"MenuText": "CTC",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Coordinates to console"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    # Mouse events
    try:
      m_ev;
    except NameError:
      m_ev=FreeCADGui.activeDocument().activeView();
      o1 = ViewObserver(m_ev);
      m_ev.addEventCallback("SoMouseButtonEvent",o1.logPosition);
  # end def
#---------------------------

FreeCADGui.addCommand('CoordsToConsol',MouseTool());
#---------------------------

#---------------------------
#This class logs any mouse button events. As the registered callback function
# fires twice for 'down' and 'up' events we need a boolean flag to handle this.
pnt1=FreeCAD.Vector(0.,0.,0.);
class ViewObserver:
  def __init__(self, view):
    self.view = view;
  # end def
  def logPosition(self, info):
    down = (info["State"] == "DOWN");
    ctrl = (info["CtrlDown"] == True);
    bttn = (info["Button"] == "BUTTON1");
    if (down and ctrl and bttn):
      pos = info["Position"];
      pnt = self.view.getPoint(pos);
      FreeCAD.Console.PrintMessage("(X,Y,Z) = "+ \
        "("+str(pnt.x)+","+str(pnt.y)+","+str(pnt.z)+")\n");
      FreeCAD.Console.PrintMessage("(dX,dY,dZ) = "+ \
        "("+str(pnt.x-pnt1.x)+","+str(pnt.y-pnt1.y)+","+ \
        str(pnt.z-pnt1.z)+")\n");
      FreeCAD.Console.PrintMessage("dR = "+ \
        str(((pnt.x-pnt1.x)**2.+(pnt.y-pnt1.y)**2.+ \
        (pnt.z-pnt1.z)**2.)**0.5)+"\n");
      pnt1.x=pnt.x; pnt1.y=pnt.y; pnt1.z=pnt.z;
      #info = self.view.getObjectInfo(pos);
      #FreeCAD.Console.PrintMessage("Object info: " + str(info) + "\n");
    # end if
  # end def
# end class
#-----------------------------------------------------

#---------------------------
class DeleteRays:
  """Screen tool object"""
  def GetResources(self):
    return {"MenuText": "DelRays",
	    #"Accel": "Ctrl+R",
	    "ToolTip": "Delete Rays"}; #,
  # end def
  def IsActive(self):
    if FreeCAD.ActiveDocument == None:
      return False;
    else:
      return True;
    # end if
  # end def
  def Activated(self):
    CalcRays.DelRays();
  # end def
#---------------------------

FreeCADGui.addCommand('DeleteRays',DeleteRays());

#---------------------------

#-----------------------------------------------------
def UpdateFunction():
  OSPropWind.hideProps();
  doc=FreeCAD.ActiveDocument;
  if (hasattr(doc,'OSData')==True):
    osd=doc.OSData;
    # full count
    FC=int(osd.getContents("B1"));
    # ray count
    RC=int(osd.getContents("C1"));
    # fill up labels
    # Optical objects
    j=4;
    while (j<RC-1):
      name1=osd.getContents(cl[3]+str(j));
      #label1=osd.getContents(cl[4]+str(j));
      if ((hasattr(doc,name1)==False)):
        osd.removeRows(str(j),1);
        # new full count
        FC=int(osd.getContents("B1"))-1;
        osd.set("B1",str(FC));
        # new ray count
        RC=int(osd.getContents("C1"))-1;
        osd.set("C1",str(RC));
        # numbers - 1
        for k in xrange(j,RC-1):
          osd.set("A"+str(k),str(int(osd.getContents('A'+str(k)))-1));
        # end for
        doc.recompute();
        j=4; # start loop again to delet another elements if needed
        continue;
      else:
        ob1=doc.getObject(name1);
        # Update Base
        v1=ob1.Placement.Base;
        if (str(v1.x)!=osd.getContents(cl[5]+str(j))):
          osd.set(cl[5]+str(j),str(v1.x));
        # end if
        if (str(v1.y)!=osd.getContents(cl[6]+str(j))):
          osd.set(cl[6]+str(j),str(v1.y));
        # end if
        if (str(v1.z)!=osd.getContents(cl[7]+str(j))):
          osd.set(cl[7]+str(j),str(v1.z));
        # end if
        # Update Rotation
        A1=ob1.Placement.Rotation.toEuler();
        if (str(A1[2])!=osd.getContents(cl[8]+str(j))):
          osd.set(cl[8]+str(j),str(A1[2]));
        # end if
        if (str(A1[1])!=osd.getContents(cl[9]+str(j))):
          osd.set(cl[9]+str(j),str(A1[1]));
        # end if
        if (str(A1[0])!=osd.getContents(cl[10]+str(j))):
          osd.set(cl[10]+str(j),str(A1[0]));
        # end if
        # Update Aperture
        if (hasattr(ob1,'Radius')==True):
          Ap1=2.*ob1.Radius.Value;
          if (str(Ap1)!=float(osd.getContents(cl[11]+str(j)))):
            osd.set(cl[11]+str(j),str(Ap1));
          # end if
        # end if
        # Update Length
        if (hasattr(ob1,'Length')==True):
          l1=ob1.Height.Value;
          if (str(l1)!=osd.getContents(cl[12]+str(j))):
            osd.set(cl[12]+str(j),str(l1));
          # end if
        # end if
        # Update Height
        if (hasattr(ob1,'Height')==True):
          h1=ob1.Height.Value;
          if (str(h1)!=osd.getContents(cl[13]+str(j))):
            osd.set(cl[13]+str(j),str(h1));
          # end if
        # end if
        # Update Thickness
        if ((ob1.Name).find('IPLT')!=-1):
          t1=(ob1.Shapes[0].Placement.Base-ob1.Shapes[1].Placement.Base).Length;
          if (str(t1)!=osd.getContents(cl[17]+str(j))):
            osd.set(cl[17]+str(j),str(t1));
          # end if
        # end if
      j=j+1;
    # end while

    # Rays
    j=RC+2;
    while (j<FC+1):
      ray1=osd.getContents(cl[3]+str(j));
      if (hasattr(doc,ray1)==False):
        osd.removeRows(str(j),1);
        FC=int(osd.getContents("B1"));
        osd.set("B1",str(FC-1));
        FreeCAD.Console.PrintMessage(str(j)+", "+str(FC-1)+"\n");
        # new full count
        FC=int(osd.getContents("B1"));
        # numbers - 1
        for k in xrange(j,FC+1):
          osd.set("A"+str(k),str(int(osd.getContents('A'+str(k)))-1));
        # end for
        doc.recompute();
        j=RC+2; # start loop again to delet another rays if needed
        continue;
      else:
        ob1=doc.getObject(ray1);
        # Update Base
        v1=ob1.Placement.Base;
        if (str(v1.x)!=osd.getContents(cl[5]+str(j))):
          osd.set(cl[5]+str(j),str(v1.x));
        # end if
        if (str(v1.y)!=osd.getContents(cl[6]+str(j))):
          osd.set(cl[6]+str(j),str(v1.y));
        # end if
        if (str(v1.z)!=osd.getContents(cl[7]+str(j))):
          osd.set(cl[7]+str(j),str(v1.z));
        # end if
        # Update Rotation
        A1=ob1.Placement.Rotation.toEuler();
        if (str(A1[2])!=osd.getContents(cl[8]+str(j))):
          osd.set(cl[8]+str(j),str(A1[2]));
        # end if
        if (str(A1[1])!=osd.getContents(cl[9]+str(j))):
          osd.set(cl[9]+str(j),str(A1[1]));
        # end if
        if (str(A1[0])!=osd.getContents(cl[10]+str(j))):
          osd.set(cl[10]+str(j),str(A1[0]));
        # end if
        # Update Color
        c1=ob1.ViewObject.LineColor;
        if (str(c1)!=osd.getContents(cl[12]+str(j))):
          osd.set(cl[12]+str(j),str(c1));
        # end if
        # Update Length
        l1=ob1.Shape.Length;
        if (str(l1)!=osd.getContents(cl[13]+str(j))):
          osd.set(cl[13]+str(j),str(l1));
        # end if
      j=j+1;
    # end while
  # end if
  doc.recompute();
  FreeCAD.Console.PrintMessage("Optical System was updated\n");
# end def
#------------------------------------------------------------------------

#--------------------------------------
# column list for OSData table
cl=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R", \
    "S","T","U","V","W","X","Y","Z"];
# Header list for OSData table
l0=["OS Numbers", "Text", "Types", "Names", "Labels", "X, mm", "Y, mm", "Z, mm", \
    "RotAX, deg.", "RotAY, deg.", "RotAZ, deg.", "Aperture, mm", \
    "Length, mm", "Width, mm", "n1", "n2", "Focus, mm", "Thickness, mm"];
lr0=["Ray Numbers","Texts", "Types", "Names", "Labels", \
     "X, mm", "Y, mm", "Z, mm", \
     "RotAX, deg.","RotAY, deg.", "RotAZ, deg.", "Wavelength, nm", \
     "Color, (R,G,B,A)","Length, mm"];
#--------------------------------------
def AddToOSData(l1,TypeStr):
  ss=CreateData('OSData');
  if (TypeStr=="Element"):
    N_fl=int(ss.getContents("B1"));
    N_rs=int(ss.getContents("C1"));
    ss.insertRows(str(N_rs-1),1);
    ss.set(cl[0]+str(N_rs-1),str(N_rs-2-2));
    for i in xrange(1,len(l0)):
      ss.set(cl[i]+str(N_rs-1),str(l1[i-1]));
    ss.set("B1",str(N_fl+1));
    ss.set("C1",str(N_rs+1));
  # end if
  if (TypeStr=="Ray"):
    N_fl=int(ss.getContents("B1"));
    N_rs=int(ss.getContents("C1"));
    ss.set(cl[0]+str(N_fl+1),str(N_fl-N_rs));
    for i in xrange(1,len(lr0)):
      ss.set(cl[i]+str(N_fl+1),str(l1[i-1]));
    # end for i
    ss.set("B1",str(N_fl+1));
  # end if
# end def
#--------------------------------------

#--------------------------------------
def CreateData(sDat):
  doc=FreeCAD.ActiveDocument;
  if (hasattr(doc,'OSData')==False):
    ss=doc.addObject('Spreadsheet::Sheet','OSData'); # add Table if no
    # create groupe and add element to it
    if (hasattr(doc,'OpticalSystem')==False):
      gr1=doc.addObject("App::DocumentObjectGroup","OpticalSystem");
      gr1.newObject("App::DocumentObjectGroup","Rays");
      gr1.newObject("App::DocumentObjectGroup","Elements");
      gr1.addObject(ss);
    else:
      gr1=getattr(doc,'OpticalSystem');
      gr1.addObject(ss);    
    # end if
    ss.set("A1","Structure:");
    FullRowCnt=6;
    ss.set("B1",str(FullRowCnt));
    RaysRowCnt=5;
    ss.set("C1",str(RaysRowCnt));
    ss.set("A2","Elements");
    ss.set("A5","Rays");
    for i in xrange(len(l0)):
      ss.set(cl[i]+str(3),str(l0[i]));
    # end for i
    for i in xrange(len(lr0)):
      ss.set(cl[i]+str(6),str(lr0[i]));
    # end for i
    doc.recompute();
    return ss;
  else:
    return doc.OSData;
  # end if
# end def
#--------------------------------------------------

#import FreeCAD,Draft;
#Draft.makeText("This is a sample text",FreeCAD.Vector(1,1,0),True);