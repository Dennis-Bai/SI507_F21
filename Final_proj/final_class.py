import requests
import json

##################################
# Common MACRO definition
##################################
YEAR_OF_INTEREST = range(2011,2021) # Search for 2011 to 2020 data


##################################
# Class definition
##################################
class articles_per_year:
    '''
        Class for 1 year's article
    '''
    def __init__(self,articles_one_year):
        self.articles = articles_one_year
    
    def top_10_cited(self):
        # Return a list of top 10 cited paper by name
        cite_cnt_dict = {}
        for paper in self.articles['articles']: 
            cite_cnt_dict[paper['title']] = paper['citing_paper_count']
        return sorted(cite_cnt_dict.items(), key=lambda x: x[1], reverse=True)

    def print_top_10(self):
        # Print the top 10 cited papers
        cite_cnt_dict = {}
        for paper in self.articles['articles']: 
            cite_cnt_dict[paper['title']] = paper['citing_paper_count']
        sorted_list = sorted(cite_cnt_dict.items(), key=lambda x: x[1], reverse=True)
        for paper in sorted_list[:10]:
            print(paper)

    def total_record(self):
        return self.articles['total_records']
    
    # def record_each_year(self):
    #     record_dict = {}
    #     for year in YEAR_OF_INTEREST:
    #         record_dict[year] = int(self.articles['total_records'])
    #     return record_dict

    def search_by_paper_name(self, paper_name):
        for paper in self.articles['articles']:
            if(paper['title'] == paper_name):
                return paper
    
    def search_by_author(self, author_name):
        paper_list = []
        for paper in self.articles['articles']:
            if (paper['authors']['authors'][0]['full_name'] == author_name):
                paper_list.append(paper)
        return paper_list



class gpu_dataset:
    '''
        Class for the whole GPU data set
    '''
    def __init__(self,all_gpu_dict):
        self.gpu_dict = all_gpu_dict
    
    def print_self(self):
        print(self.gpu_dict)

    def avg_perf_each_year(self):
        '''
            Calculate Avg performance for each year
            Return a dict that point to each year
        '''
        perf_dict = {}

        for year in YEAR_OF_INTEREST:
            perf_dict[year] = {}
        for (name,detail) in self.gpu_dict.items():
            if(detail['year'] in YEAR_OF_INTEREST):
                try:
                    perf_dict[detail['year']]['perf'] += detail['perf']
                    perf_dict[detail['year']]['cnt'] += 1
                except:
                    perf_dict[detail['year']]['perf'] = detail['perf']
                    perf_dict[detail['year']]['cnt'] = 1
        for (key,val) in perf_dict.items():
            perf_dict[key] = int(perf_dict[key]['perf'] // perf_dict[key]['cnt'])
        return list(perf_dict.values())
    
    def top_perf(self):
        top_perf_dict = {}
        for year in YEAR_OF_INTEREST:
            top_perf_dict[year] = {}
            top_perf_dict[year]['name'] = {}
            top_perf_dict[year]['perf'] = 0
            
            for (name,detail) in self.gpu_dict.items():
                if (detail['year'] == year) and (detail['perf'] >= top_perf_dict[year]['perf']):
                    top_perf_dict[year]['name'] = name
                    top_perf_dict[year]['perf'] = detail['perf']
        return(top_perf_dict)
    
    
class Node:
   def __init__(self, data):
      self.left = None
      self.right = None
      self.data = data
   def PrintTree(self):
      print(self.data)