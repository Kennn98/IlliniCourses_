from django.shortcuts import render
from course import models
from course import utility
from django.http import JsonResponse
import heapq
import random


# Create your views here.
def search(request):
    return render(request, 'search.html', {})

def course(request, subject_number):
    # format subject_number from e.g. CS411 to CS_411
    subject = []
    number = []
    for i, c in enumerate(subject_number):
        if(not c.isalpha()):
            number.extend(subject_number[i:])
            break
        subject.append(c)
    subject = ''.join(subject)
    number = ''.join(number)
    # add by zige
    coursetitle = subject_number
    subject_number = subject + "_" + number
    # test
    if(request.method == 'GET'):
        # query database
        GPA_Mapping = {"a_plus": 4.0, "a": 4.00, "a_minus": 3.67,   \
                        "b_plus": 3.33, "b": 3, "b_minus": 2.67,    \
                        "c_plus": 2.33, "c": 2.00, "c_minus": 1.67, \
                        "d_plus": 1.33, "d": 1.00, "d_minus": 0.67, \
                        "f": 0.00, "abs": 0.00, "w": 0.00}
        sql = "SELECT subject_number_id AS subject_number, year_term_id AS year_term, \
            first_name, middle_name, last_name, \
            sum(a_plus) AS a_plus, sum(a) AS a, sum(a_minus) AS a_minus, \
            sum(b_plus) AS b_plus, sum(b) AS b, sum(b_minus) AS b_minus, \
            sum(c_plus) AS c_plus, sum(c) AS c, sum(c_minus) AS c_minus, \
            sum(d_plus) AS d_plus, sum(d) AS d, sum(d_minus) AS d_minus, \
            sum(w) AS w, sum(f) AS f\
            FROM Grade \
            WHERE subject_number_id = \"{subject_number}\" \
            GROUP BY year_term_id, first_name, middle_name, last_name" \
            .format(subject_number = subject_number)

        # handle queried data
        data = utility.sqlquery(sql)
        GPA_semester = {}
        GPA_instructor = {}
        all_semester = []
        all_instructor = []
        for semester in data:
            current_semester = semester["year_term"]
            instructor_name = ' '.join([semester["first_name"], semester["middle_name"], semester["last_name"]]) \
                            if semester["middle_name"] else ' '.join([semester["first_name"], semester["last_name"]])
            if(instructor_name not in GPA_instructor):
                GPA_instructor[instructor_name] = {"total_count": 0, "total_GPA": 0}
                all_instructor.append(instructor_name)
            if(current_semester not in GPA_semester):
                GPA_semester[current_semester] = {"total_count": 0, "total_GPA": 0}
                all_semester.append(current_semester)

            for k, v in GPA_Mapping.items():
                if(k in semester):
                    GPA_semester[current_semester]["total_count"] += int(semester[k])
                    GPA_semester[current_semester]["total_GPA"] += (int(semester[k]) * v)
                    GPA_instructor[instructor_name]["total_count"] += int(semester[k])
                    GPA_instructor[instructor_name]["total_GPA"] += (int(semester[k]) * v)

        all_semester = sorted(all_semester)
        all_instructor = sorted(all_instructor)

        # query avg worload and rating
        sql = "SELECT * FROM Course WHERE subject_number = \"{subject_number}\"".format(subject_number = subject_number)
        data = utility.sqlquery(sql)
        average_workload = data[0]["average_workload"]
        average_rating = data[0]["average_rating"]

        # query tag data
        # this is the number of tags the we want for each of the return tag list
        # most freq tag: [](list of dictionary), 'content': "this is a good course", "freq": 1000, "is_selected": 0, 1
        # rand tags: same format, but its a random tag list
        ret_tag_size = 10
        most_freq_tags = []
        rand_tags = []
        total_tag_size = models.Tag.objects.filter(subject_number = subject_number).count()
        rand_tags_idx = set(random.sample(range(total_tag_size), ret_tag_size) if total_tag_size > ret_tag_size else list(range(total_tag_size)))
        heap = []
        user_name = request.user.username if request.user.is_authenticated else ""
        for idx, tag in enumerate(models.Tag.objects.filter(subject_number = subject_number).iterator()):
            truncated_tag = {"content": tag.content, "freq": len(tag.user), "selected": 1 if {"username":user_name} in tag.user else 0}
            # handle randome tag
            if(idx in rand_tags_idx):
                rand_tags.append(truncated_tag)
            # handle most freq tag
            heapq.heappush(heap, (truncated_tag["freq"], idx, truncated_tag))
            if(len(heap) >= ret_tag_size):
                heapq.heappop(heap)
        most_freq_tags = [v[2] for v in heap]

        # returned data
        # modified by zige         
        snList = []
        sgpaL = []
        for key,value in GPA_semester.items():
            snList.append(key)
            sgpaL.append(GPA_semester[key]['total_GPA'] / GPA_semester[key]['total_count'])
        inList = []
        igpaL = []
        for key,value in GPA_instructor.items():
            inList.append(key)
            igpaL.append(GPA_instructor[key]['total_GPA'] /GPA_instructor[key]['total_count'])
        ret_dic = {"GPA_semester" : sgpaL, "all_semester": snList, \
                "GPA_instructor": igpaL, "all_instructor": inList, \
                "average_workload": average_workload, "average_rating": average_rating, "subject_number": coursetitle, \
                "rand_tags": rand_tags, "most_freq_tags": most_freq_tags}
        return render(request, "course.html", ret_dic)
    # post new worklaod and rating
    elif(request.method == 'POST'):
        is_success = ""
        reason = ""
        action = request.POST.get("action", "")
        updated_rating = 5      # initial value, will be replaced later
        updated_workload = 5    # initial value, will be replaced later
        # anonymous user
        if(not request.user.is_authenticated):
            is_success = "fail"
            reason = "unauthenticated user"
        # insert or update goes here
        elif(action == "add"):
            user_name = request.user.username
            rating = int(request.POST.get("rating"))
            workload = int(request.POST.get("workload"))
            sql = "SELECT * FROM UserInput WHERE user_name = \"{user_name}\" AND subject_number_id = \"{subject_number}\"".format(user_name = user_name, subject_number = subject_number)
            data = utility.sqlquery(sql)

            # empty, need to insert new record
            if(not data):
                sql = "INSERT INTO UserInput(user_name, subject_number_id, workload, rating) VALUES (\"{user_name}\", \"{subject_number}\", {workload}, {rating})"\
                    .format(
                    user_name = user_name, subject_number = subject_number, \
                    workload = workload, rating = rating)
                print(sql)
                utility.sqlquery(sql)
            # record exist, need to update record
            else:
                sql = "UPDATE UserInput SET workload = {workload}, rating = {rating} WHERE user_name = \"{user_name}\" AND subject_number_id = \"{subject_number}\"" \
                     .format(workload = workload, rating = rating, user_name = user_name, subject_number = subject_number)
                utility.sqlquery(sql)
            # update avg rating and workload
            '''
            sql = "SELECT avg(workload) AS avg_workload FROM UserInput WHERE subject_number_id = \"{subject_number}\"".format(subject_number=subject_number)
            data = utility.sqlquery(sql)
            updated_workload = data[0]["avg_workload"] if (data and data[0]["avg_workload"]) else 5
            sql = "SELECT avg(rating) AS avg_rating FROM UserInput WHERE subject_number_id = \"{subject_number}\"".format(subject_number=subject_number)
            data = utility.sqlquery(sql)
            updated_rating = data[0]["avg_rating"] if (data and data[0]["avg_rating"]) else 5
            sql = "UPDATE Course SET average_workload = {updated_workload}, average_rating = {updated_rating} WHERE subject_number = \"{subject_number}\""\
                    .format(updated_workload = updated_workload, updated_rating = updated_rating, subject_number=subject_number)
            utility.sqlquery(sql)
            '''
            # use trigger here, do not need to update workload and rating, just grab it.
            sql = "SELECT * FROM Course WHERE subject_number = \"{subject_number}\"".format(subject_number=subject_number)
            data = utility.sqlquery(sql)
            #print("add", data)
            updated_workload, updated_rating = data[0]["average_workload"], data[0]["average_rating"]

            is_success = "success"
            reason = ""
        # delete goes here
        elif(action == "delete"):
            user_name = request.user.username
            sql = "DELETE FROM UserInput WHERE user_name = \"{user_name}\" AND subject_number_id = \"{subject_number}\"".format(user_name = user_name, subject_number = subject_number)
            utility.sqlquery(sql)
            # update avg rating and workload
            '''
            sql = "SELECT avg(workload) AS avg_workload FROM UserInput WHERE subject_number_id = \"{subject_number}\"".format(subject_number=subject_number)
            data = utility.sqlquery(sql)
            updated_workload = data[0]["avg_workload"] if (data and data[0]["avg_workload"]) else 5
            sql = "SELECT avg(rating) AS avg_rating FROM UserInput WHERE subject_number_id = \"{subject_number}\"".format(subject_number=subject_number)
            data = utility.sqlquery(sql)
            updated_rating = data[0]["avg_rating"] if (data and data[0]["avg_rating"]) else 5
            sql = "UPDATE Course SET average_workload = {updated_workload},average_rating = {updated_rating} WHERE subject_number = \"{subject_number}\""\
                    .format(updated_workload = updated_workload, updated_rating = updated_rating, subject_number=subject_number)
            utility.sqlquery(sql)
            '''
            sql = "SELECT * FROM Course WHERE subject_number = \"{subject_number}\"".format(subject_number=subject_number)
            data = utility.sqlquery(sql)
            #print("delete", data)
            updated_workload, updated_rating = data[0]["average_workload"], data[0]["average_rating"]

            is_success = "success"
            reason = ""
        # new action here: inctagcount, only need to pass tagcontent
        elif(action == "inctagcount"):
            user_name = request.user.username
            # always convert to lower case
            tag_content = (request.POST.get("tagcontent", "")).lower()
            # get the current tag model
            is_tag_exist =  models.Tag.objects.filter(subject_number = subject_number, content = tag_content).count()
            # does not allowed empty tag
            if(not tag_content):
                is_success = "fail"
                reason = "empty tag"
            # tag does not exist, create a new tag and insert into data base
            elif(is_tag_exist == 0):
                models.Tag.objects.create(
                    subject_number = subject_number,
                    subject = subject,
                    number = number,
                    content = tag_content,
                    user = [
                        {"username": user_name}
                    ]
                )
            # if tag already exist, just add name if necessary
            else:
                for t in models.Tag.objects.filter(subject_number = subject_number, content = tag_content).iterator():
                    if({"username": user_name} not in t.user):
                        t.user.append({"username": user_name})
                        t.save()
            # return the newly updated freq and random list
        # new action here dectagcount
        elif(action == "dectagcount"):
            user_name = request.user.username
            # always convert to lower case
            tag_content = (request.POST.get("tagcontent", "")).lower()
            # get the current tag model
            is_tag_exist =  models.Tag.objects.filter(subject_number = subject_number, content = tag_content).count()
            # does not allowed empty tag
            if(not tag_content):
                is_success = "fail"
                reason = "empty tag"
            # tag does not exist, create a new tag and insert into data base
            elif(is_tag_exist == 0):
                is_success = "fail"
                reason = "this tag does not exist"
            # if tag already exist, just add name if necessary
            else:
                is_success = "fail"
                reason = "user did not click this tag"
                for t in models.Tag.objects.filter(subject_number = subject_number, content = tag_content).iterator():
                    if({"username": user_name} in t.user):
                        is_success = "success"
                        reason = ""
                        if(len(t.user) > 1):
                            t.user.remove({"username": user_name})
                            t.save()
                        else:
                            t.delete()
        elif(action == "randtagrefresh"):
            user_name = request.user.username
            is_success = "success"
            reason = ""
        else:
            is_success = "fail"
            reason = "unknown action"
        # query new rand tag, and most freq tag
        ret_tag_size = 10
        most_freq_tags = []
        rand_tags = []
        total_tag_size = models.Tag.objects.filter(subject_number = subject_number).count()
        rand_tags_idx = set(random.sample(range(total_tag_size), ret_tag_size) if total_tag_size > ret_tag_size else list(range(total_tag_size)))
        heap = []
        user_name = request.user.username if request.user.is_authenticated else ""
        for idx, tag in enumerate(models.Tag.objects.filter(subject_number = subject_number).iterator()):
            truncated_tag = {"content": tag.content, "freq": len(tag.user), "selected": 1 if {"username":user_name} in tag.user else 0}
            # handle randome tag
            if(idx in rand_tags_idx):
                rand_tags.append(truncated_tag)
            # handle most freq tag
            heapq.heappush(heap, (truncated_tag["freq"], idx, truncated_tag))
            if(len(heap) >= ret_tag_size):
                heapq.heappop(heap)
        most_freq_tags = [v[2] for v in heap]
        # return the data
        ret = {"is_success": is_success, "reason": reason, "updated_rating": updated_rating, "updated_workload": updated_workload, "most_freq_tags": most_freq_tags, "rand_tags": rand_tags}
        return JsonResponse(ret)

def ranking(request):
    # use to store the data from sql query
    sql = ""
    data = []

    # query default subject list
    sql = "SELECT subject, subject_number FROM Course GROUP BY subject"
    data = utility.sqlquery(sql)
    default_subject_list = [v["subject"] for v in data]

    sql = "SELECT type FROM GeneralEducation"
    data = utility.sqlquery(sql)
    default_gened_list = [v["type"] for v in data]
    default_record_size = "20"

    # parse request data
    is_data_only = request.GET.get("isdataonly", "False")
    subject_list = request.GET.getlist("subject", default_subject_list)
    gened_list = request.GET.getlist("gened", [])
    avg_rating_lo = int(request.GET.get("avgratinglo", "0"))
    avg_rating_hi = int(request.GET.get("avgratinghi", "10"))
    avg_workload_lo = int(request.GET.get("avgworkloadlo", "0"))
    avg_workload_hi = int(request.GET.get("avgworkloadhi", "10"))
    #rating_order = request.GET.get("ratingorder", "DESC")
    #workload_order = request.GET.get("workloadorder", "ASC")
    lo = request.GET.get("lo", "0")
    hi = request.GET.get("hi", default_record_size)
    record_size = str((int(hi) - int(lo)) + 1)
    rating_keyword = request.GET.getlist("ratingkeyword", [])
    rating_order = request.GET.getlist("ratingorder", [])
    order_query = ""
    if(rating_keyword and len(rating_keyword) == len(rating_order)):
        order_query = "ORDER BY"
        buffer = []
        for keyword, order in zip(rating_keyword, rating_order):
            buffer.append(keyword + " " + order)
        order_query = order_query + " "+ ",".join(buffer)

    # do the query
    # recieved genned do the join
    if(gened_list):
        sub_query = ' AND '.join(["EXISTS(SELECT GenedSatisfaction.subject_number_id, GenedSatisfaction.type_id  FROM GenedSatisfaction \
         WHERE GenedSatisfaction.subject_number_id = Course.subject_number AND \
         GenedSatisfaction.type_id = \"{}\")".format(gened) for gened in gened_list])
        sql = "SELECT DISTINCT * \
        FROM Course\
        WHERE average_rating >= {avg_rating_lo} AND average_rating <= {avg_rating_hi} \
        AND average_workload >= {avg_workload_lo} AND average_workload <= {avg_workload_hi} \
        AND subject IN ({subject_list}) AND {sub_query} \
        {order_query} \
        LIMIT {record_size} \
        OFFSET {lo}" \
        .format(avg_rating_lo = avg_rating_lo, avg_rating_hi = avg_rating_hi,\
        avg_workload_lo = avg_workload_lo, avg_workload_hi = avg_workload_hi, \
        subject_list = ','.join(["\"" + s + "\"" for s in subject_list]), \
        sub_query = sub_query, \
        order_query = order_query, record_size = record_size, lo = lo)
    else:
        sql = "SELECT * \
        FROM Course \
        WHERE average_rating >= {avg_rating_lo} AND average_rating <= {avg_rating_hi} \
        AND average_workload >= {avg_workload_lo} AND average_workload <= {avg_workload_hi} \
        AND subject IN ({subject_list})\
        {order_query} \
        LIMIT {record_size} \
        OFFSET {lo}" \
        .format(avg_rating_lo = avg_rating_lo, avg_rating_hi = avg_rating_hi,\
        avg_workload_lo = avg_workload_lo, avg_workload_hi = avg_workload_hi, \
        subject_list = ','.join(["\"" + s + "\"" for s in subject_list]), \
        order_query = order_query, record_size = record_size, lo = lo)
    # print(sql)
    # handle the result
    all_rows = utility.sqlquery(sql)
    dic = {i:all_rows[i] for i in range(len(all_rows))}
    # send back the data
    if(True if is_data_only == "True" else False):
        return JsonResponse(dic)
    else:
        dic["default_subject_list"] = default_subject_list
        dic["default_gened_list"] = default_gened_list
        # ADDED BY ZIGE
        context = {"data": dic}
        # ADDED BY ZIGE
        return render(request, "ranking.html", context);

def error(request):
    return render(request, "error.html", {});
