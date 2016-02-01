# OptElements gui init module
# (c) 2001 Juergen Riegel LGPL

class OptElementsWorkbench (Workbench):
  "OptElements workbench object"
  MenuText = "OptElements";
  ToolTip = "OptElements workbench";
  Icon = """
 			/* XPM */
 			static const char *test_icon[]={
 			"16 16 2 1",
 			"a c #000000",
 			". c None",
 			"..############..",
 			"..#..........#..",
 			"..#..........#..",
 			"..#..........#..",
 			"..#..........#..",
 			"..#..........#..",
 			"..############..",
 			"................",
 			"..############..",
 			"..#.............",
 			"..#.............",
 			"..############..",
 			"..#.............",
 			"..#.............",
 			"..############..",
 			"................"};
			""";
  def Initialize(self):
    # load the module
    import OptElementsGui;
    self.appendToolbar("ControlTools", ["OSPropTool","ElPropTool","UpdateOS", \
      "CalculateRayPropag"]);
    self.appendToolbar("OptTools", ["CreateRay","DeleteRays","CreateLens", \
      "CreateMirror", "CreateScreen",'CreateInterface','CreatePlate', \
        'ElBuildTool']);
#    self.appendToolbar("OptBuilder", ['ElBuildTool']);
    self.appendToolbar("ControlTools", ["SetOrientZXFitAll", \
      "SetOrientZX",'CoordsToConsol']);
    self.appendMenu("OptTools", ["UpdateOS","SetOrientZXFitAll","OSPropTool", \
      "ElPropTool","DeleteRays","CreateRay","CreateLens","CreateMirror", \
      "CreateScreen",'CreateInterface','CreatePlate','CoordsToConsol',
      'ElBuildTool']);
    Log("Loading OptElements module... done\n");
  
  def GetClassName(self):
    return "Gui::PythonWorkbench";
  
  def Activated(self):
    # do something here if needed...
    Msg("OptElementsWorkbench.Activated()\n");
  
  def Deactivated(self):
    # do something here if needed...
    Msg("OptElementsWorkbench.Deactivated()\n");

Gui.addWorkbench(OptElementsWorkbench());
