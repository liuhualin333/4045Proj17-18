import matplotlib.pyplot as plt
_x = [0.16475485966504269, 0.66477521642660053, 0.2354803658938433, 0.022161404769264755, 0.12407135506570902, 0.052960508510996776, 0.46948671930270958, 0.1007185403407623, 1.5217192865111715, 0.19394387191626064, 1.9951712633828704, 0.44329106684252745, 0.74079056775266106, 0.32236672817847051, 1.6728241239412651, 0.12385311430969788, 0.33499375913540291, 0.26519184914470711, 0.59919427088462618, 0.33930950432416584, 1.5106517696470982, 1.2726879788590677, 0.065593624441974224, 0.05160609787897813, 0.88467148131843099, 0.13540391463326235, 0.067971318035940823, 0.5435467232161364, 0.35992322222537737, 0.51246142132355532, 0.072801511385457179, 1.4504557226267507, 0.1540552622507454, 0.24283217465400359, 0.53746740271848881, 0.80035232579245019, 0.024457569740688266, 0.98751647217688776, 0.16752940271687516, 0.5209000032941713, 0.071093876850937154, 0.67977176615914792, 0.12448618947398296, 1.3600823889493567, 0.1310328397760703, 0.65405014574742848, 0.34661004638191839, 1.1348493263874635, 0.069190114831435015, 0.06504931595170578]
_y = [0.10247963394624669, 0.00086435004087273841, 0.053058775817271121, 0.0048469550607795316, 0.029552123797699188, 0.0002686360376397715, 0.0047792965843199749, 0.037748438780580457, 0.0077804285147507887, 0.091824345165687993, 0.037631022109616934, 0.076527144543317063, 0.22340382472209352, 0.055202494471302134, 0.043412917493769729, 0.017973333042263003, 0.02236406560211494, 0.0073294799423531294, 0.06171814001628996, 0.0014159914364973991, 0.028001648310961039, 0.033060612463168798, 0.023075105540564678, 0.0016156907681426263, 0.0088609219982726233, 0.10594242977110722, 0.067215701923544632, 0.013614620444686336, 0.0041089717220499531, 0.036089454083471161, 0.013888435624653004, 0.0079710378946578949, 0.027141920155599027, 0.20272429652860735, 0.013507113866489241, 0.055239359533996793, 0.084820342272732274, 0.013915890014465519, 0.0066662312958635384, 0.11890611836300342, 0.032854419968109901, 0.063456505747565325, 0.15104209824384662, 0.015521948610446371, 0.021619801157903556, 0.015110152308958036, 0.052568388486678011, 0.0012499639815022425, 0.013275545353450999, 0.063918010764010255]
_c = [0.9672751701414783, 0.9671590121408667, 0.9676738377282547, 0.9703858418046052, 0.9675907673468225, 0.9713045459671757, 0.9687655479524332, 0.9680983217619018, 0.9683820659129008, 0.967748578049899, 0.966706348369657, 0.966439701250429, 0.9659789014450054, 0.9673528491044932, 0.9677203325840066, 0.9679280043342362, 0.9673627470894289, 0.9685215908335998, 0.9669514002147359, 0.9689902000651462, 0.9681333524013179, 0.9665888649989272, 0.9679291681106138, 0.9690687118680804, 0.967032375263021, 0.9664624196133718, 0.9673096689873811, 0.9672967940307955, 0.9686610148035439, 0.9676509165731568, 0.9682780635645116, 0.9679982195512254, 0.9685807872973287, 0.9661598782638512, 0.9673217288032687, 0.9668289117180445, 0.9672376531423779, 0.9676446485064045, 0.9687105899390762, 0.9669636744059834, 0.9673885191652946, 0.9676138394809485, 0.9666416712676841, 0.967089231011954, 0.9679114263119369, 0.9674738889121314, 0.967653983496005, 0.9678736546119742, 0.9687337788679238, 0.9687801413329464]
plt.style.use('ggplot')
fig = plt.figure()
fig.set_size_inches(12, 12)
ax = plt.gca()
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('C1')
ax.set_ylabel('C2')
ax.set_title("Randomized Hyperparameter Search CV Results (min={:0.3}, max={:0.3})".format(
    min(_c), max(_c)
))

ax.scatter(_x, _y, c=_c, s=60, alpha=0.9, edgecolors=[0,0,0])
fig.show()

print("Dark blue => {:0.4}, dark red => {:0.4}".format(min(_c), max(_c)))
input()