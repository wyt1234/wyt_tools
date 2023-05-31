import time
import traceback
import urllib3
import pymongo
from multiprocessing import Process, Queue, set_start_method

from bson import ObjectId
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from retrying import retry
from tqdm import trange
from datetime import datetime
from DB_ONLINE import create_patent_merge_connection, create_patent_dupl_connection, create_patent_assignee_connection, \
    create_patent_applicant_connection, create_patent_inventor_connection
from queue import Empty

'''专利数据：同步Mongo中到ES'''

es1 = Elasticsearch(["es地址", ])

def find_in_mongo(queue1: Queue):
    col = create_patent_merge_connection()

    with col.find({}).batch_size(500) as cursor:
        all_data_count = col.estimated_document_count()
        for _ in trange(all_data_count):
            data = cursor.next()

            queue1.put(data)


def find_dupl_data_in_mongo(queue1: Queue, queue2: Queue):
    while True:
        try:
            data = queue1.get(timeout=3600)
        except Empty:
            break
        except:
            traceback.print_exc()
            continue
        dupl_col = create_patent_dupl_connection()
        dupl_id = ObjectId(data.get("dupl_id"))
        dupl_data = dupl_col.find_one({"_id": dupl_id})
        if dupl_data:
            queue2.put([dupl_data, data])


@retry(stop_max_attempt_number=100)
def write_es(actions, es):
    helpers.bulk(es, actions)


def update_patent(queue2: Queue, es):
    ass_col = create_patent_assignee_connection()
    app_col = create_patent_applicant_connection()
    inv_col = create_patent_inventor_connection()
    actions = []
    count = 0
    while True:
        try:
            data, merge_data = queue2.get(timeout=3600)
            count += 1

            _id = str(data.get("_id"))

            app_date = data.get("app_date", None)
            if app_date and type(app_date) == int and len(str(app_date)) == 8:
                try:
                    app_date = datetime.strptime(str(app_date), "%Y%m%d").isoformat() + "Z"
                except:
                    app_date = None
            else:
                app_date = None

            pub_date = data.get("pub_date", None)
            if pub_date and type(pub_date) == int and len(str(pub_date)) == 8:
                try:
                    pub_date = datetime.strptime(str(pub_date), "%Y%m%d").isoformat() + "Z"
                except:
                    pub_date = None
            else:
                pub_date = None

            auth_date = data.get("auth_date", None)
            if auth_date and type(auth_date) == int and len(str(auth_date)) == 8:
                try:
                    auth_date = datetime.strptime(str(auth_date), "%Y%m%d").isoformat() + "Z"
                except:
                    auth_date = None
            else:
                auth_date = None

            ep_family_id = data.get("ep_family_id", [])

            app_kind = data.get("app_kind", None)

            pub_kind = data.get("pub_kind", None)
            if pub_kind in ["公表特許公報(A)","公開特許公報(A)"]:
                pub_kind = "A"

            app_num = data.get("app_num", None)

            country = data.get("country", None)

            pub_num = data.get("pub_num", None)

            auth_num = data.get("auth_num", None)

            app_search_id = country + app_num

            pub_search_id = country + pub_num + pub_kind

            patent_id = country + app_num + pub_kind

            applicant_raw = data.get("applicant", None)
            if applicant_raw and type(applicant_raw) == list:
                applicant_dupl_data = app_col.find({"patent_id": _id})
                applicant = []
                for app in applicant_dupl_data:
                    applicant_temp = {}
                    raw_address_info = app.get("raw_address_info")
                    if raw_address_info:
                        AddressInfo = {"raw": raw_address_info}
                        applicant_temp["AddressInfo"] = AddressInfo
                    org_id = app.get("org_id")
                    if org_id:
                        applicant_temp["org_id"] = org_id
                    applicant_temp["name"] = app.get("name") if app.get("name") else 0
                    applicant.append(applicant_temp)
            else:
                applicant = []
            inventor_raw = data.get("inventor", None)
            if inventor_raw and type(inventor_raw) == list:
                inventor_dupl_data = inv_col.find({"patent_id": _id})
                inventor = []
                for app in inventor_dupl_data:
                    inventor_temp = {}
                    raw_address_info = app.get("raw_address_info")
                    if raw_address_info:
                        AddressInfo = {"raw": raw_address_info}
                        inventor_temp["AddressInfo"] = AddressInfo
                    person_id = app.get("person_id")
                    if person_id:
                        inventor_temp["person_id"] = person_id
                    inventor_temp["name"] = app.get("name") if app.get("name") else 0
                    inventor.append(inventor_temp)
            else:
                inventor = []

            assignee_raw = data.get("assignee", None)
            if assignee_raw and type(assignee_raw) == list:
                assignee_dupl_data = ass_col.find({"patent_id": _id})
                assignee = []
                for app in assignee_dupl_data:
                    assignee_temp = {}
                    raw_address_info = app.get("raw_address_info")
                    if raw_address_info:
                        AddressInfo = {"raw": raw_address_info}
                        assignee_temp["AddressInfo"] = AddressInfo
                    org_id = app.get("org_id")
                    if org_id:
                        assignee_temp["org_id"] = org_id
                    assignee_temp["name"] = app.get("name") if app.get("name") else 0
                    assignee.append(assignee_temp)
            else:
                assignee = []

            abstract_ls = data.get("abstract", None)
            if abstract_ls and type(abstract_ls) == list:
                abstract = {}
                for abstract_d in abstract_ls:
                    abstract[abstract_d.get("lang")] = abstract_d.get("content")
            else:
                abstract = {}

            # claims_ls = data.get("claims", None)
            # if claims_ls and type(claims_ls) == list:
            #     claims = {}
            #     for claims_d in claims_ls:
            #         claims[claims_d.get("lang")] = claims_d.get("content")
            # else:
            #     claims = {}

            title_ls = data.get("title", None)
            if title_ls and type(title_ls) == list:
                title = {}
                for title_d in title_ls:
                    title[title_d.get("lang")] = title_d.get("content")
            else:
                title = {}

            priority_ls = data.get("priority", None)
            if priority_ls and type(priority_ls) == list:
                priority = []
                for pro in priority_ls:
                    priority_temp = {"country": pro.get(country)}
                    date = pro.get(country)
                    if date and type(date) == int and len(str(date)) == 8:
                        try:
                            date = datetime.strptime(str(date), "%Y%m%d").isoformat() + "Z"
                            priority_temp["date"] = date
                        except:
                            pass
                    priority_temp["num"] = pro.get("num")
                    priority.append(priority_temp)
            else:
                priority = []

            ipc_ls = data.get("ipc", None)
            if ipc_ls and type(ipc_ls) == list:
                ipc = []
                for ipcs in ipc_ls:
                    ipc_temp = {"l1": ipcs.get("l1", ""), "l2": ipcs.get("l2", ""), "l3": ipcs.get("l3", ""),
                                "l4": ipcs.get("l4", "")}
                    ipc.append(ipc_temp)
            else:
                ipc = []

            cpc_ls = data.get("cpc", None)
            if cpc_ls and type(cpc_ls) == list:
                cpc = []
                for cpcs in cpc_ls:
                    cpc_temp = {"l1": cpcs.get("l1", ""), "l2": cpcs.get("l2", ""), "l3": cpcs.get("l3", ""),
                                "l4": cpcs.get("l4", ""), "raw": cpcs.get("raw", "")}
                    cpc.append(cpc_temp)
            else:
                cpc = []

            ipcr_ls = data.get("ipcr", None)
            if ipcr_ls and type(ipcr_ls) == list:
                ipcr = []
                for ipcrs in ipcr_ls:
                    ipcr_temp = {"l1": ipcrs.get("l1", ""), "l2": ipcrs.get("l2", ""), "l3": ipcrs.get("l3", ""),
                                 "l4": ipcrs.get("l4", "")}
                    ipcr.append(ipcr_temp)
            else:
                ipcr = []

            pct_ls = data.get("pct_info", None)
            if pct_ls and type(pct_ls) == list:
                pct = []
                for pc in pct_ls:
                    pct_temp = {"app_num": pc.get("application_number", None),
                                "pub_num": pc.get("publication_number", None)}
                    pct.append(pct_temp)
            else:
                pct = []

            patent_family_id = merge_data.get("family_id", [])

            other_kind_version_is_exist = merge_data.get("all_version")
            if other_kind_version_is_exist:
                if len(other_kind_version_is_exist) <= 1:
                    other_kind_version_dic = []
                else:
                    other_kind_version_dic = []
                    for kind in other_kind_version_is_exist:
                        if _id != other_kind_version_is_exist[kind]:
                            other_kind_version_dic.append({kind: other_kind_version_is_exist[kind]})
            else:
                other_kind_version_dic = []

            tmp = {
                "app_date": app_date,
                "app_kind": app_kind,
                "app_num": app_num,
                "abstract": abstract,
                "app_search_id": app_search_id,
                "applicant": applicant,
                "assignee": assignee,
                "auth_date": auth_date,
                "auth_num": auth_num,
                "id" : patent_id,
                # "claims": claims,
                "country": country,
                "cpc": cpc,
                "ep_family_id": ep_family_id,
                "inventor": inventor,
                "ipc": ipc,
                "ipcr": ipcr,
                "pct": pct,
                "priority": priority,
                "pub_date": pub_date,
                "pub_kind": pub_kind,
                "pub_num": pub_num,
                "pub_search_id": pub_search_id,
                "title": title,
                "patent_family_id": patent_family_id,
                "other_kind_version": other_kind_version_dic
            }
            actions.append({
                "_index": "patent_v3",
                "_name": "_doc",
                "_id": _id,
                "_source": tmp
            })

            if count % 1000 == 0:
                try:
                    write_es(actions, es)
                    actions = []
                except:
                    traceback.print_exc()
                    actions = []
                    continue
        except Empty:
            if count % 1000 > 0:
                helpers.bulk(es, actions)
            print("task_done")
            break
        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    urllib3.disable_warnings()
    # set_start_method('fork')
    queues1 = Queue(1000)
    queues2 = Queue(1000)
    p_ls = []

    for _ in range(1):
        p1 = Process(target=find_in_mongo, args=(queues1,))
        p_ls.append(p1)
    for _ in range(10):
        p1 = Process(target=find_dupl_data_in_mongo, args=(queues1, queues2,))
        p_ls.append(p1)
    for _ in range(20):
        p1 = Process(target=update_patent, args=(queues2, es1,))
        p_ls.append(p1)
    for p in p_ls:
        p.start()
    for p in p_ls:
        p.join()
