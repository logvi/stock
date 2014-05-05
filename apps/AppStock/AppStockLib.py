# coding: utf-8
__author__ = 'vitalijlogvinenko'
import datetime
import csv
import urllib, urlparse
from django.utils.timezone import utc
from .models import Ticker, finam_tickers
from itertools import groupby
from lxml import html
from django.db import IntegrityError


#Класс для выгрузки биржевых данных
class AppStockUpload:
    #Выгрузка из сайта mfd
    def uploadFromMFD(self, ObjName, categoryId, Tickers, startDate, endDate, period):
        if startDate is None:
            startDate = '01.01.2004'
        if endDate is None:
            endDate = datetime.datetime.now()
            endDate = datetime.datetime.strftime(endDate, "%d.%m.%Y")
        TF = {"H1":6, "D":7, "W":8, "M":9}
        #Готовим ссылку
        url = "http://mfd.ru/export/handler.ashx/mfdexport_1day_01012004_15042014.txt?TickerGroup=16&Tickers=63%2C64%2C65%2C66%2C28336%2C28432%2C68%2C45272%2C45273%2C59994%2C62792%2C59998%2C59817%2C59990%2C59992%2C54116%2C61157%2C59993%2C59995%2C51987%2C61775%2C59186%2C69%2C70%2C60508%2C42358%2C46778%2C57580%2C33231%2C33232%2C44732%2C56693%2C59816%2C29363%2C51903%2C51900%2C51901%2C51902%2C51914%2C71%2C17125%2C49748%2C41379%2C51821%2C50793%2C41928%2C9834%2C42020%2C72%2C51947%2C39233%2C47446%2C29901%2C50794%2C40145%2C47447%2C50994%2C39605%2C32144%2C58241%2C57590%2C37399%2C56252%2C54106%2C44598%2C118%2C17799%2C17800%2C73%2C74%2C27760%2C27759%2C27806%2C33197%2C30447%2C39682%2C35646%2C39683%2C28430%2C28431%2C124%2C123%2C9477%2C16371%2C27808%2C28887%2C28886%2C28885%2C30459%2C28888%2C28889%2C27909%2C131%2C29628%2C17764%2C45230%2C133%2C134%2C16488%2C135%2C136%2C137%2C138%2C140%2C139%2C141%2C142%2C143%2C144%2C100%2C101%2C102%2C18021%2C48903%2C41369%2C41479%2C27802%2C27803%2C15996%2C9248%2C29059%2C29060%2C157%2C28370%2C36362%2C168%2C158%2C159%2C169%2C41480%2C41481%2C170%2C172%2C171%2C107%2C108%2C109%2C13999%2C110%2C9761%2C173%2C174%2C175%2C178%2C177%2C111%2C113%2C112%2C35281%2C17338%2C15995%2C182%2C183%2C27755%2C59129%2C14963%2C199%2C200%2C27906%2C27907%2C204%2C45229%2C28600%2C28601%2C211%2C212%2C213%2C214%2C215%2C216%2C41228%2C41229%2C49714%2C49718%2C49715%2C49719%2C49720%2C49716%2C49721%2C49717%2C49722%2C217%2C40761%2C227%2C228%2C232%2C27812%2C27811%2C16112%2C51884%2C9086%2C51851%2C27765%2C27810%2C187%2C27788%2C27787%2C236%2C237%2C28396%2C28397%2C239%2C240%2C41482%2C41483%2C188%2C189%2C190%2C17293%2C191%2C41807%2C27813%2C27814%2C241%2C193%2C194%2C195%2C196%2C31135%2C41981%2C41982%2C27927%2C27928%2C244%2C51864%2C246%2C273%2C276%2C277%2C28376%2C281%2C27756%2C27757%2C252%2C27881%2C287%2C288%2C293%2C294%2C291%2C28543%2C28544%2C292%2C289%2C290%2C27768%2C27779%2C28372%2C28373%2C28584%2C28585%2C28586%2C28587%2C28588%2C28589%2C304%2C305%2C28590%2C28591%2C307%2C306%2C27753%2C27754%2C56478%2C28368%2C28369%2C310%2C311%2C308%2C309%2C316%2C317%2C27828%2C321%2C322%2C27965%2C27966%2C27967%2C27968%2C27969%2C27970%2C258%2C257%2C28564%2C16128%2C32863%2C32340%2C32339%2C32342%2C32341%2C264%2C28576%2C28577%2C28578%2C28579%2C28580%2C28581%2C265%2C266%2C267%2C269%2C48800%2C48801%2C29037%2C51883%2C270%2C28411%2C28412%2C42052%2C42053%2C27740%2C42056%2C40089%2C27798%2C42605%2C61131%2C346%2C330%2C40087%2C42057%2C42663%2C42662%2C38822%2C352%2C353%2C354%2C355%2C356%2C357%2C358%2C359%2C360%2C361%2C362%2C363%2C364%2C365%2C366%2C367%2C368%2C369%2C370%2C371%2C372%2C373%2C374%2C375%2C376%2C377%2C46551%2C51850%2C27830%2C27831%2C27832%2C27833%2C336%2C15428%2C51856%2C34618%2C28423%2C342%2C27834%2C27835%2C395%2C396%2C397%2C399%2C400%2C27915%2C27916%2C27917%2C27918%2C27919%2C27920%2C27921%2C27922%2C27923%2C27924%2C27925%2C27926%2C403%2C404%2C27766%2C27776%2C27795%2C27796%2C31351%2C383%2C51849%2C57307%2C29046%2C44517%2C388%2C9120%2C38756%2C17798%2C415%2C416%2C391%2C392%2C393%2C394%2C15168%2C424%2C438%2C9249%2C448%2C57591%2C42055%2C41824%2C27885%2C27886%2C41825%2C36443%2C443%2C444%2C29038%2C55259%2C17765%2C17766%2C445%2C15166%2C50968%2C446%2C51921%2C43788%2C53333%2C46805%2C51913%2C44733%2C51942%2C53203%2C51943%2C47065%2C28392%2C28393%2C464%2C465%2C27839%2C27840%2C466%2C467%2C41489%2C41490%2C27744%2C27783%2C41488%2C41486%2C41487%2C470%2C65447%2C471%2C9976%2C473%2C475%2C474%2C477%2C478%2C479%2C51885%2C17810%2C488%2C489%2C490%2C37332%2C491%2C492%2C49273%2C49274%2C50956%2C50957%2C17107%2C16370%2C494%2C495%2C496%2C497%2C499%2C15662%2C51887%2C460%2C27746%2C27751%2C506%2C461%2C54955%2C55017%2C64989%2C61245%2C64409%2C64990%2C65665%2C462%2C545%2C27841%2C27913%2C28343%2C548%2C550%2C28371%2C555%2C511%2C27964%2C27963%2C34936%2C558%2C559%2C560%2C561%2C28426%2C29055%2C29058%2C519%2C27816%2C27817%2C571%2C572%2C573%2C574%2C520%2C42049%2C521%2C525%2C528%2C529%2C49900%2C581%2C580%2C41491%2C27735%2C27872%2C27873%2C27807%2C27842%2C582%2C41810%2C534%2C28350%2C535%2C586%2C587%2C589%2C41809%2C28394%2C28395%2C591%2C592%2C540%2C28436%2C28437%2C602%2C598%2C27730%2C599%2C605%2C606%2C607%2C608%2C541%2C542%2C611%2C612%2C614%2C38032%2C49583%2C615%2C28927%2C28676%2C47480%2C616%2C41969%2C41967%2C41968%2C48811%2C49088%2C41492%2C41493%2C27818%2C27819%2C28363%2C28364%2C620%2C619%2C621%2C622%2C543%2C544%2C643%2C14995%2C647%2C64410%2C27741%2C27775%2C650%2C648%2C653%2C652%2C41230%2C40946%2C28360%2C660%2C659%2C41496%2C41497%2C629%2C632%2C633%2C634%2C27843%2C27844%2C27910%2C27887%2C635%2C636%2C637%2C41498%2C666%2C31760%2C31761%2C832%2C17326%2C42385%2C833%2C838%2C28398%2C28399%2C840%2C841%2C41813%2C669%2C27845%2C27846%2C672%2C673%2C15557%2C854%2C49747%2C855%2C856%2C61457%2C16349%2C9820%2C862%2C9060%2C35831%2C51876%2C17105%2C27888%2C27889%2C28335%2C27849%2C716%2C28563%2C35101%2C879%2C28410%2C28413%2C881%2C880%2C41970%2C51353%2C893%2C46788%2C33490%2C27847%2C889%2C27971%2C27848%2C27734%2C891%2C892%2C9441%2C726%2C728%2C27905%2C729%2C730%2C731%2C732%2C733%2C734%2C735%2C736%2C737%2C738%2C739%2C740%2C741%2C742%2C743%2C744%2C745%2C746%2C49089%2C747%2C750%2C751%2C752%2C753%2C754%2C755%2C756%2C757%2C758%2C759%2C760%2C761%2C762%2C763%2C764%2C765%2C766%2C767%2C768%2C769%2C770%2C771%2C772%2C773%2C774%2C775%2C776%2C778%2C777%2C779%2C780%2C781%2C782%2C783%2C784%2C785%2C786%2C787%2C788%2C789%2C790%2C791%2C792%2C793%2C794%2C795%2C796%2C797%2C798%2C799%2C800%2C41499%2C801%2C802%2C803%2C804%2C805%2C806%2C807%2C808%2C809%2C810%2C811%2C812%2C813%2C814%2C815%2C816%2C817%2C818%2C819%2C820%2C821%2C36230%2C28325%2C28326%2C826%2C41971%2C41972%2C35613%2C51860%2C905%2C906%2C39588%2C28414%2C28415%2C944%2C945%2C41973%2C940%2C27853%2C40846%2C909%2C910%2C40845%2C913%2C915%2C916%2C917%2C948%2C28351%2C28407%2C28408%2C951%2C952%2C949%2C950%2C29702%2C27749%2C41974%2C27784%2C41975%2C957%2C35798%2C27851%2C27852%2C27738%2C27850%2C27747%2C962%2C963%2C927%2C928%2C29036%2C964%2C15813%2C27854%2C28545%2C965%2C47661%2C28508%2C28509%2C28510%2C28511%2C28512%2C967%2C968%2C969%2C28513%2C970%2C28514%2C28515%2C28516%2C28517%2C971%2C973%2C28449%2C974%2C28454%2C28455%2C28450%2C28451%2C28452%2C28453%2C975%2C28481%2C978%2C979%2C28327%2C54550%2C53204%2C984%2C42015%2C17763%2C17762%2C985%2C40762%2C43149%2C27771%2C27770%2C989%2C990%2C992%2C18048%2C1000%2C1001%2C993%2C17145%2C27729%2C41401%2C41402%2C28418%2C28419%2C1004%2C1005%2C27820%2C27772%2C45274%2C1006%2C1007%2C27804%2C27805%2C42084%2C1013%2C41500%2C35502%2C35501%2C1014%2C40833%2C28400%2C28401%2C1263%2C1264%2C1265%2C1266%2C41503%2C41504%2C57251%2C43712%2C42051%2C1271%2C1273%2C1272%2C27762%2C27739%2C51220%2C51221%2C47454%2C1275%2C41501%2C41814%2C41815%2C41816%2C41817%2C41818%2C41819%2C1019%2C46251%2C60069%2C1021%2C1022%2C1023%2C1024%2C1026%2C1027%2C1025%2C1028%2C1029%2C1030%2C1031%2C51886%2C1033%2C15018%2C58629%2C1034%2C37247%2C1035%2C1036%2C39670%2C51923%2C51881%2C1037%2C1038%2C51894%2C1039%2C1044%2C1041%2C1040%2C1042%2C1043%2C51915%2C37255%2C51324%2C1045%2C51935%2C31603%2C1046%2C14000%2C1047%2C1048%2C51896%2C51905%2C31064%2C1049%2C1050%2C1053%2C9265%2C1051%2C1052%2C31063%2C31062%2C1054%2C1055%2C51862%2C1056%2C38034%2C1057%2C40940%2C49569%2C51857%2C51940%2C64418%2C46522%2C36267%2C1058%2C1072%2C31082%2C52515%2C1059%2C1060%2C1061%2C1062%2C1063%2C1064%2C1065%2C1066%2C1067%2C1068%2C51934%2C1069%2C1070%2C1071%2C51861%2C1073%2C1074%2C1075%2C1076%2C1077%2C1078%2C1079%2C1080%2C1081%2C1082%2C1083%2C47417%2C37775%2C51930%2C51950%2C53332%2C1084%2C51951%2C51325%2C51326%2C51323%2C51906%2C51865%2C51924%2C51899%2C51874%2C51873%2C1085%2C51963%2C51897%2C51922%2C51868%2C30470%2C43360%2C40214%2C51909%2C52598%2C1086%2C51879%2C51290%2C1087%2C43735%2C1088%2C1089%2C51960%2C31616%2C28603%2C48769%2C1091%2C49749%2C48766%2C60067%2C36849%2C51322%2C1090%2C51908%2C63511%2C33759%2C51937%2C33758%2C61829%2C1092%2C51932%2C38821%2C1093%2C1094%2C41249%2C18029%2C35832%2C1095%2C51945%2C1096%2C1097%2C31443%2C37256%2C1098%2C1099%2C49189%2C51911%2C1101%2C10132%2C51880%2C1102%2C49259%2C51617%2C51918%2C15047%2C28890%2C39684%2C1103%2C51867%2C51895%2C1104%2C1105%2C51822%2C34535%2C1106%2C32450%2C38033%2C30371%2C1107%2C1100%2C46521%2C43709%2C1108%2C33556%2C1109%2C51891%2C51866%2C51869%2C31084%2C51858%2C1110%2C31083%2C51948%2C47416%2C1111%2C1112%2C1119%2C41404%2C1120%2C1121%2C9153%2C31065%2C1122%2C1123%2C1124%2C1125%2C1126%2C10133%2C1127%2C51888%2C1134%2C51321%2C51954%2C1128%2C1129%2C1130%2C1132%2C1131%2C51904%2C1133%2C44735%2C33195%2C1113%2C45571%2C51291%2C62499%2C28962%2C42988%2C1135%2C1114%2C1115%2C51898%2C1116%2C1136%2C16432%2C1137%2C60068%2C31617%2C51907%2C1117%2C1118%2C36517%2C51920%2C1139%2C1140%2C1141%2C1142%2C1143%2C1144%2C44504%2C44505%2C1145%2C1138%2C51852%2C1146%2C51910%2C1147%2C1148%2C1149%2C1150%2C30472%2C1154%2C1153%2C1151%2C1152%2C1155%2C1156%2C35928%2C51938%2C33418%2C1160%2C32155%2C28926%2C51941%2C51926%2C43711%2C43713%2C51958%2C1161%2C1162%2C60491%2C51957%2C43014%2C1164%2C30469%2C30471%2C1163%2C1165%2C51917%2C1166%2C1167%2C28604%2C51959%2C1168%2C51956%2C35285%2C1169%2C51955%2C51889%2C46543%2C51946%2C50789%2C1170%2C16606%2C1157%2C1158%2C1159%2C52027%2C31136%2C46012%2C51227%2C1171%2C64417%2C1172%2C1184%2C1185%2C51949%2C1186%2C1187%2C53461%2C48767%2C1183%2C61827%2C47429%2C51927%2C1173%2C1174%2C1175%2C1176%2C1177%2C1188%2C51893%2C1178%2C1179%2C51962%2C51928%2C1189%2C27974%2C17285%2C51966%2C1190%2C51892%2C1191%2C1182%2C1180%2C1181%2C1192%2C52414%2C52413%2C52424%2C52419%2C52418%2C53132%2C52409%2C52416%2C52411%2C52422%2C52421%2C52420%2C52415%2C52423%2C52417%2C30372%2C51964%2C1193%2C52599%2C38741%2C51936%2C51890%2C1194%2C1195%2C51944%2C31602%2C1196%2C51863%2C9763%2C1197%2C31615%2C64451%2C1198%2C31022%2C36848%2C49923%2C1201%2C1202%2C1203%2C1204%2C1207%2C1208%2C1205%2C1209%2C1210%2C1206%2C1211%2C37254%2C1212%2C1213%2C1214%2C46737%2C41251%2C51953%2C1215%2C28602%2C51878%2C30299%2C1199%2C1200%2C31714%2C36847%2C49190%2C49191%2C1216%2C1217%2C1218%2C1219%2C1220%2C51961%2C51929%2C1222%2C1224%2C1223%2C1225%2C1221%2C47648%2C1226%2C51853%2C1227%2C61828%2C51919%2C27904%2C44503%2C51916%2C1228%2C42661%2C1229%2C41381%2C41370%2C48768%2C1230%2C51859%2C36266%2C1233%2C51939%2C1232%2C63510%2C31445%2C1231%2C51925%2C1235%2C17996%2C1238%2C1234%2C51854%2C1237%2C1236%2C9033%2C9390%2C17949%2C39228%2C43806%2C1240%2C1241%2C41502%2C1279%2C1281%2C1243%2C35956%2C1284%2C1285%2C1286%2C1287%2C1288%2C1289%2C27778%2C28409%2C17327%2C1294%2C58189%2C43367%2C48946%2C1297%2C28606%2C43807%2C1246%2C1247%2C1248%2C1300%2C27731%2C27752%2C30375%2C1250%2C1251%2C51931%2C1252%2C1254%2C1255%2C1256%2C1257%2C1352%2C1353%2C1303%2C27911%2C27912%2C1304%2C1359%2C35301%2C28353%2C1308%2C1307%2C27895%2C27890%2C46667%2C33408%2C62535%2C30373%2C1310%2C46596%2C28416%2C28417%2C61060%2C59991%2C1311%2C1312%2C28607%2C1360%2C1361%2C1362%2C1363%2C1364%2C1365%2C1366%2C1367%2C1368%2C51871%2C51872%2C51967%2C28331%2C28332%2C28333%2C28334%2C1326%2C1327%2C58324%2C58325%2C1370%2C33481%2C17794%2C1372%2C28427%2C31085%2C1334%2C1373%2C54102%2C54103%2C1383%2C1384%2C36376%2C36377%2C36378%2C36379%2C36380%2C36381%2C36382%2C36383%2C36384%2C36385%2C36386%2C36387%2C36388%2C36389%2C36390%2C36391%2C27733%2C27748%2C27855%2C27856%2C49258%2C1385%2C1386%2C1380%2C1381%2C1337%2C1338%2C58323%2C1341%2C33198%2C16407%2C31679%2C36571%2C48895%2C63600%2C1389%2C30298%2C57601%2C58322%2C1402%2C1393%2C41334%2C41929%2C28561%2C17328%2C28404%2C1413%2C1412%2C28303%2C27857%2C27858%2C27777%2C27767%2C27859%2C27860%2C40765%2C40766%2C27972%2C27973%2C27743%2C27799%2C27800%2C27801%2C41494%2C41495%2C28329%2C41339%2C41340%2C28330%2C27791%2C27792%2C27789%2C27790%2C27764%2C27780%2C1463%2C28546%2C1464%2C54930%2C27862%2C27861%2C1467%2C27745%2C1465%2C1466%2C17106%2C1469%2C1479%2C1476%2C9808%2C39756%2C40947%2C46738%2C45199%2C28424%2C28425%2C1418%2C27865%2C27864%2C27866%2C27867%2C27868%2C27869%2C1419%2C1420%2C9251%2C16114%2C1492%2C1493%2C1494%2C27896%2C27863%2C1487%2C1488%2C32947%2C1495%2C1496%2C1498%2C17797%2C1497%2C1502%2C1503%2C1506%2C30018%2C40779%2C51933%2C1434%2C28405%2C28406%2C28386%2C28387%2C1509%2C1510%2C1511%2C1512%2C28344%2C1515%2C42082%2C1516%2C42081%2C1437%2C28428%2C28429%2C1526%2C1527%2C1528%2C1529%2C1445%2C9252%2C1530%2C27908%2C1536%2C9391%2C9087%2C1448%2C1542%2C1543%2C17240%2C31023%2C1600%2C1545%2C28361%2C28362%2C1606%2C1607%2C1604%2C1605%2C1547%2C41820%2C41821%2C1608%2C1609%2C30463%2C1610%2C1612%2C1613%2C1614%2C1615%2C28388%2C28389%2C1624%2C1625%2C1622%2C1623%2C1549%2C1554%2C28547%2C28548%2C1557%2C1558%2C1559%2C28518%2C28519%2C28520%2C28521%2C28522%2C28523%2C28524%2C1551%2C1552%2C1553%2C1560%2C1561%2C1562%2C1563%2C1564%2C1565%2C28549%2C28550%2C28551%2C1566%2C28525%2C28526%2C28527%2C1567%2C1568%2C28592%2C28477%2C28593%2C28478%2C28468%2C28479%2C28469%2C28480%2C28470%2C28594%2C28471%2C28472%2C28473%2C28474%2C28475%2C28476%2C1570%2C1571%2C1572%2C1573%2C1575%2C28483%2C28501%2C28484%2C28502%2C28485%2C28503%2C28486%2C28504%2C28487%2C28505%2C28488%2C28506%2C28489%2C28507%2C28490%2C28491%2C28492%2C28493%2C28494%2C28495%2C28496%2C28497%2C28498%2C28499%2C28500%2C1576%2C28439%2C28440%2C28441%2C28442%2C28443%2C28444%2C28445%2C28582%2C1577%2C1578%2C1579%2C28438%2C28552%2C28553%2C28554%2C28555%2C28556%2C28557%2C28558%2C28559%2C28560%2C1580%2C1582%2C28456%2C28457%2C28458%2C28459%2C28460%2C28461%2C28462%2C28463%2C28583%2C1584%2C1585%2C1586%2C1587%2C28464%2C28465%2C28466%2C28467%2C28572%2C28573%2C1626%2C40778%2C1588%2C41505%2C41811%2C41812%2C32421%2C41279%2C1593%2C59801%2C30648%2C32451%2C32452%2C27736%2C27737%2C1638%2C1639%2C27891%2C27892%2C27761%2C1640%2C1641%2C1598%2C1599%2C41822%2C35278%2C31759%2C1658%2C65189%2C1645%2C1646%2C1647%2C29054%2C51120%2C44507%2C35282%2C40684%2C41252%2C17118%2C1648%2C14964%2C14965%2C9937%2C63579%2C14966%2C43015%2C33196%2C42054%2C37269%2C37270%2C1660%2C27824%2C27825%2C1659%2C61741%2C28366%2C28367%2C27781%2C27782%2C1665%2C1681%2C27769%2C27875%2C27876%2C28390%2C28391%2C1683%2C1684%2C1688%2C1689%2C33749%2C34898%2C27826%2C27827%2C41930%2C1691%2C1692%2C27713%2C1693%2C1694%2C33760%2C1670%2C1690%2C51912%2C27878%2C1701%2C1702%2C41980%2C17760%2C17761%2C27879%2C27880%2C27758%2C37444%2C37445%2C1706%2C45200%2C16589%2C16588%2C16590%2C1678%2C27809%2C27897%2C28337%2C1664%2C41976%2C41977%2C41978%2C41979%2C27877%2C1718%2C27829%2C41403%2C51965%2C51855%2C16369%2C1710%2C16113%2C1711%2C51952%2C51870%2C51882%2C42083%2C43023%2C13955%2C56692%2C37859%2C1712%2C30448%2C31618%2C28324%2C27836%2C28352%2C27837%2C27838%2C41965%2C41966%2C1733%2C1734%2C35055%2C1745%2C1748%2C1738%2C1739%2C27943%2C27944%2C27945%2C27946%2C27947%2C27948%2C27949%2C27950%2C27951%2C27952%2C27953%2C27954%2C27955%2C27956%2C27957%2C27958%2C27959%2C27960%2C27961%2C27962%2C27929%2C27930%2C27931%2C27932%2C27933%2C27934%2C27935%2C27936%2C27937%2C27938%2C27939%2C27940%2C27941%2C27942%2C1741%2C28402%2C28403%2C27870%2C27871%2C1759%2C1760%2C1757%2C1758%2C1763%2C1765%2C1764%2C41959%2C27763%2C27815%2C1767%2C1768%2C1749%2C41484%2C41485%2C1750%2C1753%2C1754%2C1755%2C37883%2C41960%2C27773%2C27821%2C27785%2C27786%2C41808%2C27822%2C27823%2C28328%2C27794%2C1786%2C16408%2C16409%2C30082%2C41962%2C41963%2C41964%2C41961%2C41231%2C27732%2C27884%2C51877%2C1801%2C1802%2C51875%2C1803%2C1805%2C28323%2C27750%2C27914%2C27742%2C27774%2C27893%2C27894%2C1796%2C1797%2C1798%2C27874%2C44777%2C28562%2C1818%2C1820%2C1811%2C1812%2C1813%2C27882%2C27883%2C27793%2C27797%2C1828%2C1826%2C1827%2C28374%2C28375%2C34958%2C1830%2C1831%2C41823&Alias=false&Period=7&timeframeValue=1&timeframeDatePart=day&StartDate=01.01.2004&EndDate=15.04.2014&SaveFormat=0&SaveMode=0&FileName=mfdexport_1day_01012004_15042014.txt&FieldSeparator=%253b&DecimalSeparator=.&DateFormat=yyyyMMdd&TimeFormat=HHmmss&DateFormatCustom=&TimeFormatCustom=&AddHeader=false&RecordFormat=0&Fill=false"
        scheme, netloc, path, query_string, fragment = urlparse.urlsplit(url)
        query = urlparse.parse_qs(query_string)
        b = {
            'Tickers':[str(Tickers)[1:-1]],
            'EndDate':[endDate],
            'StartDate':[startDate],
            'Period':[str(TF[period])]
        }
        query.update(b)
        new_query = urllib.urlencode(query,True)
        new_url = urlparse.urlunsplit((scheme, netloc, path, new_query, fragment))
        print(new_url)
        file = urllib.urlopen(new_url)
        #print(file.read().decode("utf-8"))
        #Импортируем из csv
        reader = csv.reader(file, delimiter = ';')
        # for row in reader:
        #     print row[1] + "; " + row[2] + "; " + row[3] + "; " + row[4] + "; " + row[5] + "; " + row[6] + "; " + row[7]
        for row in reader:
            d = datetime.datetime.strptime(row[2],'%Y%m%d')
            t = datetime.datetime.strptime(row[3],'%H%M%S')
            ticker = Ticker.objects.get_or_create(name=str(row[0]),category_id=categoryId)
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            q = ObjName.objects.get_or_create(
                #category_id = categoryId,
                ticker_id = ticker[0].id,
                per = row[1],
                date = d.date(),
                time = d.time(),
                defaults={
                    'date_create':now,
                    'open' : row[4],
                    'hight' : row[5],
                    'low' : row[6],
                    'close' : row[7],
                    'vol' : row[8]
                }
            )
            Ticker.objects.filter(id=ticker[0].id).update(last_update=now)
        return True
    #Конец функции uploadFromMFD
    #**

    #Функция для загрузки из Финама
    def uploadFromFinam(self, obj, categoryId, Tickers, startDate, endDate, period):
        if startDate is None:
            startDate = '01.04.2004'
        if endDate is None:
            endDate = datetime.datetime.now()
            #endDate = datetime.datetime.strftime(endDate, "%d.%m.%Y")
        else:
             endDate = datetime.datetime.strptime(endDate, "%d.%m.%Y")
        startDate = datetime.datetime.strptime(startDate, "%d.%m.%Y")
        TF = {"H1":7, "D":8, "W":9, "M":10}
        #Готовим ссылку
        url = "http://195.128.78.52/SBER_130516_140429.txt?market=1&em=3&code=SBER&df=16&mf=4&yf=2013&dt=29&mt=3&yt=2014&p=8&f=SBER_130516_140429&e=.txt&cn=SBER&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&datf=1"
        scheme, netloc, path, query_string, fragment = urlparse.urlsplit(url)
        query = urlparse.parse_qs(query_string)
        #df - день начала
        #mf - месяц начала
        #yf - год начала
        #dt - день конец
        #mt - месяц конец
        #yt - год конец
        #p - период (7 - часовик, 8 - D, 9 - W, 10 - M)
        #em - id тикера
        #datf - формат записи
        b = {
            'em':[str(Tickers)[1:-1]],
            'df':[str(startDate.day)],
            'mf':[str(startDate.month - 1)],
            'yf':[str(startDate.year)],
            'dt':[str(endDate.day)],
            'mt':[str(endDate.month - 1)],
            'yt':[str(endDate.year)],
            'p':[str(TF[period])]
        }
        query.update(b)
        new_query = urllib.urlencode(query,True)
        s = new_query.split('&')
        market = 0
        for i,row in enumerate(s):
            if(row.split('=')[0] == 'market'):
                market = i
                break
        if market!=0:
            temp = s[0]
            s[0] = s[market]
            s[market] = temp
        new_query = '&'.join(s)
        new_url = urlparse.urlunsplit((scheme, netloc, path, new_query, fragment))
        print(new_url)
        file = urllib.urlopen(new_url)
        #print(file.read().decode('utf-8'))
        #Импортируем из csv
        for row in file.readlines():
            s = row.decode('utf-8')
            a = s.split(';')
            d = datetime.datetime.strptime(a[2],'%Y%m%d')
            t = datetime.datetime.strptime(a[3],'%H%M%S')
            ticker = finam_tickers.objects.get(finam_id=Tickers[0])
            #ticker = Ticker.objects.get_or_create(name=str(row[0]),category_id=categoryId)
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            #Если обновляемая котировка отличается от аналогичной в базе то апдейтим её
            try:
                k = obj.objects.get(
                    ticker_id = ticker.ticker_id,
                    per = a[1],
                    date = d.date(),
                    time = d.time(),
                    open = a[4],
                    hight = a[5],
                    low = a[6],
                    close = a[7],
                    vol = a[8]
                )
                print('OK')
            except obj.DoesNotExist:
            #апдейтим либо создаём
                self.update_or_create(obj,{
                    'ticker_id' : ticker.ticker_id,
                    'per' : a[1],
                    'date' : d.date(),
                    'time' : d.time() },
                    {
                    'date_create':now,
                    'open' : a[4],
                    'hight' : a[5],
                    'low' : a[6],
                    'close' : a[7],
                    'vol' : a[8]
                })
                print('update')
                Ticker.objects.filter(id=ticker.ticker_id).update(last_update=now)
        # reader = csv.reader(file.read().decode('utf-8'), delimiter=';')
        # for row in reader:
        #     print(str(row))
            #print (str(row[1]) + "; " + row[2] + "; " + row[3] + "; " + row[4] + "; " + row[5] + "; " + row[6] + "; " + row[7])
        return True

    #Функция для парсинга id тикеров из сайта Финама или mfd
    #На вход нужен файл в формате txt с html кодом списка тикеров
    def getTickersFromHTML(self, file, css_attr='li a'):
        res = []
        file = open(file)
        lines = file.read().decode('utf-8')
        doc = html.document_fromstring(lines)
        for li in doc.cssselect(css_attr):
            res.append({"id":li.get("value"),"value": li.text})
        return res

    #Функци для загрузки id тикеров из финама или mfd ко мне в базу
    def loadTickersFromHTML(self, file, obj, css_attr='li a', field_id='finam_id'):
        t = self.getTickersFromHTML(file, css_attr)
        for row in t:
            print(row['value'] + " = " + row['id'])
            self.update_or_create(obj, {'name':row['value']}, {'name':row['value'],field_id:row['id']})

    #Функция "обновить или создать"
    def update_or_create(self, model, filter_kwargs, update_kwargs):
        try:
            k = model.objects.get(**filter_kwargs)
            model.objects.filter(**filter_kwargs).update(id=k.id,**update_kwargs)
        except model.DoesNotExist:
            print('not')
            kwargs = filter_kwargs.copy()
            kwargs.update(update_kwargs)
            print(kwargs)
            try:
                model.objects.create(**kwargs)
            except IntegrityError:
                if not model.objects.filter(**filter_kwargs).update(**update_kwargs):
                    raise  # re-raise IntegrityError

#Конец класса AppStockUpload
#**

#Класс для биржевых индикаторов
class AppStockIndicators:

    #Вычисление EMA
    #period - коэффициэнт сглаживаня
    #rounded - округлять или нет (до 4 знаков)
    #field - для словаря, поле откуда брать значение
    #output - для словаря, возвращать значение в словарь list в поле output
    def EMA(self, list, period, rounded = True, field = 'close', output = None):
        res = []
        if (type(list[0]) != dict):
            x = list[0]
        else:
            x = list[0][str(field)]
        res.append(self._ema_calc(x,0,period,rounded,output))
        if(output is not None):
            list[0][str(output)] = res[0]
        i = 1
        while i<len(list):
            if (type(list[i]) != dict):
                x = list[i]
            else:
                x = list[i][str(field)]
            res.append(self._ema_calc(x,res[i-1],period,rounded,output))
            if(output is not None):
                list[i][str(output)] = res[i]
            i += 1
        if(output is not None):
            return list
        else:
            return res
    #Конец функции EMA
    #**

    #Вспомогательная функция для EMA
    def _ema_calc(self, x, y, period, rounded=True, output = None):
        #Если возвращаем в словарь формируем res для словаря
        k = float(2.0/(period+1))
        if(output is not None):
            if y != 0:
                y = y['ema']
            else:
                y = x
            a = x*k + y*(1-k)
            if(rounded):
                res = {'ema':round(a,4), 'period':period}
            else:
                res = {'ema':a, 'period':period}
        #Иначе делаем обычный массив
        else:
            if y == 0:
                y = x
            a = x*k + y*(1-k)
            if(rounded):
                res = round(a,4)
            else:
                res = a
        return res
    #Конец _ema_calc
    #**

    #Функция для вычисления слеждующего значения EMA
    def nextEMA(self, row, ema_row, fieldPrice, fieldEMA, rounded=True):
        res = self._ema_calc(row[fieldPrice], ema_row[fieldEMA], ema_row[fieldEMA]['period'], rounded, output=fieldEMA)
        output = fieldEMA
        res_row = row
        res_row[str(output)] = res
        return res_row
    #Конец nextEMA
    #**

    #Функция для вычисления SMA
    def SMA(self, rs, period, rounded=True, field='close', output=None):
        res = []
        i = 0
        #print(rs)
        while i<len(rs):
            #print(str(i)+" = "+str(rs[i]))
            if (type(rs[i]) != dict):
                x = sum(rs[(i-period)+1:i+1])
            else:
                x = 0
                if((i-period)+1>=0):
                    x = sum(item[str(field)] for item in rs[(i-period)+1:i+1])
            sma = float(x/period)
            if(rounded):
                sma = round(sma, 4)
            #print("sma = "+str(sma))
            if(output is not None):
                res.append({'sma':sma, 'period':period})
                rs[i][str(output)] = res[i]
            else:
                res.append(sma)
            i += 1
        if(output is not None):
            return rs
        else:
            return res
    #Конец функции SMA
    #**

    #Вспомогательная функия
    def _sma_calc(self, x, y, pre_sma, period, rounded):
        sma = 0
        if(pre_sma!=0):
            a = float(y/period - x/period)
            sma = pre_sma - a
        if(rounded):
            sma = round(sma, 4)
        return sma
    #Конец _sma_calc
    #**

    #Для вычисления следующего значения SMA
    def nextSMA(self, row, pre_rs, fieldPrice, fieldEMA, rounded=True):
        print(pre_rs)
        l_pre_rs = pre_rs[len(pre_rs)-1]
        print(str(l_pre_rs))
        period = l_pre_rs[fieldEMA]['period']
        print(" period = "+str(period))
        y = pre_rs[len(pre_rs)-period][fieldPrice]
        pre_sma = l_pre_rs[fieldEMA]['sma']
        sma = self._sma_calc(row[str(fieldPrice)], y, pre_sma, period, rounded)
        res = row
        res[fieldEMA] = {'sma':sma, 'period':period}
        return res
    #Конец nextSMA
    #**

    #Вычисление MACD
    #output - возвращать в list в поле output
    def MACD(self, list, EMA1, EMA2, period, field = 'close', output = None):
        delta = []
        ema1 = self.EMA(list, EMA1, field=field)
        ema2 = self.EMA(list, EMA2, field=field)
        i = 0
        while i<len(ema1):
            delta.append({'fast': (ema1[i] - ema2[i]), 'ema1':{'ema':ema1[i],'period':EMA1}, 'ema2':{'ema':ema2[i],'period':EMA2}})
            i += 1
        res = self.EMA(delta, period, False, 'fast', 'signal')
        if(output is not None):
            i = 0
            while i<len(list):
                list[i][str(output)] = res[i]
                i += 1
            return list
        else:
            return res
    #Конец функции MACD
    #**

    #Функция для вычисления следующего MACD
    def nextMACD(self, row, pre_row, fieldPrice, fieldMACD, rounded=True):
        price = row[fieldPrice]
        row_macd = pre_row[fieldMACD]
        ema1 = self._ema_calc(price, row_macd['ema1'], row_macd['ema1']['period'], rounded, output='1')
        ema2 = self._ema_calc(price, row_macd['ema2'], row_macd['ema2']['period'], rounded, output='1')
        delta = {'fast': (ema1['ema'] - ema2['ema']), 'ema1':ema1, 'ema2':ema2}
        signal = self._ema_calc(delta['fast'], row_macd['signal'], row_macd['signal']['period'], rounded=False, output=fieldMACD)
        delta['signal'] = signal
        res_row = row
        res_row[fieldMACD] = delta
        return res_row
    #Конец nextMACD
    #**

class TestAppStockIndicators(AppStockIndicators):

    def testEMA(self, obj):
        indicators = AppStockIndicators()
        qs = obj.objects.filter(per='D',ticker_id=4,date__gte='2012-09-13',date__lte='2014-04-21').order_by('date').values('close','date','low','per','hight')
        res = indicators.EMA(qs, 150, rounded=False, field='close', output='ema150')


