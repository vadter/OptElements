import FreeCAD, Draft;

# column list for OSData table
cl=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R", \
    "S","T","U","V","W","X","Y","Z"];

#------------------------------------------------------------------------
def CalculateFunction():
  doc=FreeCAD.ActiveDocument;
  doc.recompute();
  if (hasattr(doc,'OSData')==True):
    osd=doc.OSData;
    RC=int(osd.getContents("C1"));
    FC=int(osd.getContents("B1"));
    # Delete all old Rays (DWires)
    DelRays();
    # Point List
    PL=[];
    # Rays loop
    i=RC+2;
    while (i<FC+1):
      ray1=doc.getObject(osd.getContents(cl[3]+str(i)));
      # Point of the current ray
      Pr=ray1.Shape.Curve.StartPoint;
      # Vector of the current ray
      Vr=ray1.Shape.Curve.EndPoint-Pr;
      Vr=Vr*(1./Vr.Length);
      PL+=[Pr];
      # Optical objects loop
      j=4;
      while (j<RC-1):
        ob1=doc.getObject(osd.getContents(cl[3]+str(j)));
        # Changing Direction
        # Lenses
        if (osd.getContents(cl[4]+str(j)).find('PLEN')!=-1):
          # Point on the surface of optical object
          Pob=ob1.Placement.Base;
          # Normal at the point on the surface
          uv = ob1.Shape.Surface.parameter(Pob);
          Nob = ob1.Shape.normalAt(uv[0],uv[1]);
          Nob=Nob*(1./Nob.Length);
          # Calculate point of intersection
          proj1=Vr*Nob;
          if (proj1!=0.):
            length1=((Pob-Pr)*Nob)/proj1;
            if (length1<100000.):
              Pint=Pr+Vr*length1;
              PL+=[Pint];
              # New section start point
              Pr=Pint;
            else:
              Pint=Pr+Vr*10.;
              break;
            # end if
          # end if
          # Vector in plane of object
          Vi=Pint-Pob; ei=FreeCAD.Vector(Vi);
          if (Vi.Length!=0.):
            ei=ei*(1./ei.Length);
          else:
            j=j+1;
            continue;
          # end if
          if (Vi.Length<ob1.Radius):
            # Unity vector perpendicular to Nob and ei in plane of object
            epi=Nob.cross(ei);
            # Decomposition of Vr on two projection along vectors Nob, ei, epi 
            Vn=Nob*Vr; Vei=ei*Vr; Vpi=epi*Vr;
            f1=float(osd.getContents(cl[16]+str(j)));
            # Finding an angles of falling on the surface
            Vei=-Vi.Length/f1+Vei;
            # New section direction
            Vr=Nob*Vn+ei*Vei+epi*Vpi;
          else:
            #Vr=None;
            break;
          # end if
        # end if
        # Mirror
        if (osd.getContents(cl[4]+str(j)).find('MIR')!=-1):
          # Point on the surface of optical object
          Pob=ob1.Placement.Base;
          # Normal at the point on the surface
          uv = ob1.Shape.Surface.parameter(Pob);
          Nob = ob1.Shape.normalAt(uv[0],uv[1]);
          Nob=Nob*(1./Nob.Length);
          # Calculate point of intersection
          proj1=Vr*Nob;
          if (proj1!=0.):
            length1=((Pob-Pr)*Nob)/proj1;
            if (length1<100000.):
              Pint=Pr+Vr*length1;
              PL+=[Pint];
              # New section start point
              Pr=Pint;
            else:
              Pint=Pr+Vr*10.;
              break;
            # end if
          # Vector in plane of object
          Vi=Pint-Pob;
          if (Vi.Length<ob1.Radius):
            # Decomposition of Vr on projection along vector Nob
            Vn=Nob*Vr;
            # Reflection
            Vr=Vr-Nob*(2.*Vn);
          else:
            #Vr=None;
            break;
          # end if
        # Interface
        if (osd.getContents(cl[4]+str(j)).find('INT')!=-1):
          # Point on the surface of optical object
          Pob=ob1.Placement.Base;
          # Normal at the point on the surface
          uv = ob1.Shape.Surface.parameter(Pob);
          Nob = ob1.Shape.normalAt(uv[0],uv[1]);
          Nob=Nob*(1./Nob.Length);
          # Calculate point of intersection
          proj1=Vr*Nob;
          if (proj1!=0.):
            length1=((Pob-Pr)*Nob)/proj1;
            if (length1<100000.):
              Pint=Pr+Vr*length1;
              PL+=[Pint];
              # New section start point
              Pr=Pint;
            else:
              Pint=Pr+Vr*10.;
              break;
            # end if
          # end if
          # Vector perpendicular to the incident plane.
          epi=Nob.cross(Vr);
          if (epi.Length!=0.):
            epi=epi*(1./epi.Length);
          # end if
          # Vector in the incident plane.
          ei=Nob.cross(epi);
          # Projection in the incident plane
          Vei=ei*Vr; Vn=Nob*Vr;
          n1=float(osd.getContents(cl[14]+str(j)));
          n2=float(osd.getContents(cl[15]+str(j)));
          Vei=Vei*n1/n2;
          sqr1=1.-Vei**2.;
          if (sqr1>=0.):
            # refraction
            Vn=(sqr1)**0.5*(Vn/abs(Vn));
            Vr=Nob*Vn+ei*Vei;
          else:
            # Reflection (total internal)
            Vr=Vr-Nob*(2.*Vn);
          # end if
        # end if
        # Screen
        if (osd.getContents(cl[4]+str(j)).find('SCR')!=-1):
          # Point on the surface of optical object
          Pob=ob1.Placement.Base;
          # Normal at the point on the surface
          uv = ob1.Shape.Surface.parameter(Pob);
          Nob = ob1.Shape.normalAt(uv[0],uv[1]);
          Nob=Nob*(1./Nob.Length);
          # Calculate point of intersection
          proj1=Vr*Nob;
          if (proj1!=0.):
            length1=((Pob-Pr)*Nob)/proj1;
            if (length1<100000.):
              Pint=Pr+Vr*length1;
              PL+=[Pint];
              # New section start point
              Pr=Pint;
            else:
              Pint=Pr+Vr*10.;
              break;
            # end if
          break;
        # end if
        # Bulk Elements
        if ((osd.getContents(cl[4]+str(j)).find('BLEN')!=-1) or \
            (osd.getContents(cl[4]+str(j)).find('BPRISM')!=-1) or \
            (osd.getContents(cl[4]+str(j)).find('IPLT')!=-1) or \
            (osd.getContents(cl[4]+str(j)).find('IMPR')!=-1) or \
            (osd.getContents(cl[4]+str(j)).find('BPLT')!=-1)):
          # Refractive indexes
          n1=float(osd.getContents(cl[14]+str(j))); # out of element
          n2=float(osd.getContents(cl[15]+str(j))); # inside the element
          # Finding of all points of intersection with faces
          # and then to find the least length from Pr 
          # List of all faces          
          f1=ob1.Shape.Faces;
          err1=1.e-3;
          # Cycle on faces
          for m in xrange(0,len(f1)):
            Lf1=[];
            # Internal cycle on faces
            for k in xrange(0,len(f1)):
#              FreeCAD.Console.PrintMessage(str(type(f1[k].Surface).__name__)+"-----\n");
              if (type(f1[k].Surface).__name__=='GeomPlane'):
                # Point on plane
                P1=f1[k].Surface.Position;
                # Normal
                N1=f1[k].Surface.Axis;
                # Calculate point of intersection
                proj1=Vr*N1;
                if (proj1!=0.):
                  l1=((P1-Pr)*N1)/proj1;
                  P1=Pr+Vr*l1;
                  if ((ob1.Shape.isInside(P1,err1,True)==True) and \
                    (l1>1.e-3)):
                    if (ob1.Shape.isInside(P1-Vr*4.*err1,err1,True)==False):
                      Lf1+=[[P1,N1,'in']];
                    else:
                      Lf1+=[[P1,N1,'out']];
#                      FreeCAD.Console.PrintMessage(str(Lf1[-1])+"\n");
                    # end if
                  # end if
                # end if
              # end if
              if (type(f1[k].Surface).__name__=='GeomSphere'):
                V2=Vr.Length**2.;
                Ps=f1[k].Surface.Center;
                R=f1[k].Surface.Radius; R2=R**2.;
                PsmP=Ps-Pr; PsmP2=PsmP.Length**2.;
                PsmPV=(Ps-Pr)*Vr; PsmPV2=PsmPV**2.;
                sqr1=PsmPV2-(PsmP2-R2)*V2;
                if (sqr1>=0.):
                  sqrt1=(sqr1)**0.5;
                  l1=(PsmPV-sqrt1)/V2;
                  P1=Pr+Vr*l1;
                  if ((ob1.Shape.isInside(P1,err1,True)==True) and \
                    (l1>0.001)):
                    # normal for sphere
                    N1=(P1-Ps); N1=N1*(1./N1.Length);
                    if (ob1.Shape.isInside(P1-Vr*4.*err1,err1,True)==False):
                      Lf1+=[[P1,N1,'in']];
                    else:
                      Lf1+=[[P1,N1,'out']];
                    # end if
                  #end if
                  l2=(PsmPV+sqrt1)/V2;
                  P2=Pr+Vr*l2;
                  if ((ob1.Shape.isInside(P2,err1,True)==True) and \
                    (l2>0.001)):
                    # normal for sphere
                    N2=(P2-Ps); N2=N2*(1./N2.Length);
                    if (ob1.Shape.isInside(P2-Vr*4.*err1,err1,True)==False):
                      Lf1+=[[P2,N2,'in']];
                    else:
                      Lf1+=[[P2,N2,'out']];
                    # end if
                  #end if
                # end if
              #end if
              if (type(f1[k].Surface).__name__=='GeomCylinder'):
                V2=Vr.Length**2.;
                Pc=f1[k].Surface.Center;
                R=f1[k].Surface.Radius; R2=R**2.;
                Vc=f1[k].Surface.Axis;
                # rotation vector
                rot1=FreeCAD.Rotation(Vc,FreeCAD.Vector(0.,0.,1.));
                rot2=FreeCAD.Rotation(FreeCAD.Vector(0.,0.,1.),Vc);
                P0=rot1.multVec(Pr); V0=rot1.multVec(Vr);
                Pc0=rot1.multVec(Pc);
                PcmP0=Pc0-P0; PcmP0.z=0.; PcmP02=PcmP0.Length**2.;
                V0xy=FreeCAD.Vector(V0); V0xy.z=0.; V0xy2=V0xy.Length**2.;
                if (V0xy2!=0.):
                  sqr1=(PcmP0*V0xy)**2.-(PcmP02-R2)*V0xy2;
                  if (sqr1>=0.):
                    t1=(PcmP0*V0xy-(sqr1)**0.5)/V0xy2;
                    # point of intersection in displaced coordinate system
                    P01=P0+V0*t1;
                    # in initial CS
                    P1=rot2.multVec(P01);
                    # normal in the point of intersection 
                    # in displaced coordinate system                    
                    N01=(P01-Pc0); N01=N01*(1./N01.Length); N01.z=0.;
                    # in initial CS
                    N1=rot2.multVec(N01);
                    if (N1!=FreeCAD.Vector(0.,0.,0.)):
                      N1=N1*(1./N1.Length);
                    # end if
                    if ((ob1.Shape.isInside(P1,err1,True)==True) and \
                      (t1>0.001)):
                      if (ob1.Shape.isInside(P1-Vr*4.*err1,err1,True)==False):
                        Lf1+=[[P1,N1,'in']];
                      else:
                        Lf1+=[[P1,N1,'out']];
                      # end if
                    # end if
                    t2=(PcmP0*V0xy+(sqr1)**0.5)/V0xy2;
                    # point of intersection in displaced coordinate system
                    P02=P0+V0*t2;
                    # in initial CS
                    P2=rot2.multVec(P02);
                    # normal in the point of intersection 
                    # in displaced coordinate system                    
                    N02=(P02-Pc0); N02=N02*(1./N02.Length); N02.z=0.;
                    # in initial CS
                    N2=rot2.multVec(N02);
                    if (N2!=FreeCAD.Vector(0.,0.,0.)):
                      N2=N2*(1./N2.Length);
                    # end if
                    if ((ob1.Shape.isInside(P2,err1,True)==True) and \
                      (t2>0.001)):
                      if (ob1.Shape.isInside(P2-Vr*4.*err1,err1,True)==False):
                        Lf1+=[[P2,N2,'in']];
                      else:
                        Lf1+=[[P2,N2,'out']];
                      # end if
                    # end if
                  # enf if
                # end if
              # end if
              if (type(f1[k].Surface).__name__=='GeomCone'):
                Cone1=True;
              # end if
              if (type(f1[k].Surface).__name__=='GeomToroid'):
                Torus1=True;
              # end if
              if (type(f1[k].Surface).__name__=='GeomBSplineSurface'):
                Pr1=FreeCAD.Vector(Pr);
#                V1=Pr-PL[-1];
                # Intersection with bounding box of the BSpline
#                if ((Vr*V1>0.) and (f1[k].BoundBox.intersect(Pr,Vr)==True)):
                for i1 in xrange(0,5):
                  UV1=f1[k].Surface.parameter(Pr1);
                  # Point of the nearest orthogonal projection
                  Pop1=f1[k].Surface.value(UV1[0],UV1[1]);
                  # Vector of the nearest orthogonal projection
                  Vop1=Pop1-Pr1;
                  if (Vop1.Length>1.e-3):
                    if (Vr*Vop1>0):
                      Pr1=Pr1+Vr*Vop1.Length;
                    else:
                      Pr1=Pr1-Vr*Vop1.Length;
                    # end if
                  else:
                    break;
                  # end if
                # end for i1
#                # end if
                V1=Pr1-Pr;
                if ((V1.Length>1.e-3) and (V1*Vr>0.) and \
                  (ob1.Shape.isInside(Pr1,err1,True)==True)):
                  uv = f1[k].Surface.parameter(Pr1);
                  Nr1= f1[k].normalAt(uv[0],uv[1]);
                  Nr1=Nr1*(1./Nr1.Length);
                  if (ob1.Shape.isInside(Pr1-Vr*4.*err1,err1,True)==False):
                    Lf1+=[[Pr1,Nr1,'in']];
#                    FreeCAD.Console.PrintMessage(str(Lf1[-1])+"\n");
                  else:
                    Lf1+=[[Pr1,Nr1,'out']];
#                    FreeCAD.Console.PrintMessage(str(Lf1[-1])+"\n");
              # end if
#              FreeCAD.Console.PrintMessage(str(type(f1[k].Surface).__name__)+"\n");
            # end for k
            # Finding closest
            if (Lf1!=[]):
#              FreeCAD.Console.PrintMessage(str(Lf1)+"\n");
              Lf2=Lf1[0];
              for p in xrange(1,len(Lf1)):
                if ((Lf1[p][0]-Pr).Length<(Lf2[0]-Pr).Length):
                  Lf2=Lf1[p];
                # end if
              # end for p
#              FreeCAD.Console.PrintMessage(str(Lf2)+"\n");
              # Add the shortest length to list of intersection points
              Pr=Lf2[0];
              # Protection of close points
              if ((PL[-1]-Pr).Length>1.e-3):              
                PL+=[Pr];
              # end if
              # Changing direction of the ray Vr
              # Normal
              Nob=Lf2[1];
              # Vector perpendicular to the incident plane.
              epi=Nob.cross(Vr);
              if (epi.Length!=0.):
                epi=epi*(1./epi.Length);
              # end if
              # Vector in the incident plane.
              ei=Nob.cross(epi);
              # Projection in the incident plane
              Vei=ei*Vr; Vn=Nob*Vr;
              if (Lf2[2]=='in'):
                Vei=Vei*n1/n2;
              else:
                Vei=Vei*n2/n1;
              # end if
              sqr1=1.-Vei**2.;
              if (sqr1>=0.):
                # refraction
                Vn=(sqr1)**0.5*(Vn/abs(Vn));
                Vr=Nob*Vn+ei*Vei;
              else:
                # Reflection (total internal)
                Vr=Vr-Nob*(2.*Vn);
              # end if
            # end if
          # end for m
        # end if
        j=j+1;
      # end while j
      w1=Draft.makeWire(PL);
      if (hasattr(doc,'Rays')==True):
        gr1_e=getattr(doc,'Rays');
        gr1_e.addObject(w1);
      # end if
      w1.ViewObject.LineWidth=1.;
      w1.ViewObject.LineColor=ray1.ViewObject.LineColor;
      w1.Label="Ray"+ray1.Label;
      PL=[];
      i=i+1;
    # end while i
    doc.recompute();
    FreeCAD.Console.PrintMessage("Rays is calculated\n");
  # end if
# end def
#--------------------------------------

#--------------------------------------------------
def DelRays():
  """ Delete all old Rays (DWires) """
  doc=FreeCAD.ActiveDocument;
  i=0;
  while (i<len(doc.Objects)):
    ob1=doc.Objects[i];
    if ((ob1.Label).find('RayIR')!=-1):
      doc.removeObject(ob1.Name);
      continue;
    # end if
    i=i+1;
  # end while i
# end def