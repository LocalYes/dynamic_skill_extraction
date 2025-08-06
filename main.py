from extraction_step import skill_extraction_step
from utils.skill_extraction import init_client
import concurrent.futures
import time

PARAMS= {
    "extract_model": "gpt-4.1-mini",
    "embed_model": "text-embedding-3-large",
    "topk": 4,
    "skills_embed_data": "ESCO_single_string_ONET_tech.pkl",
    "client": None
}

def extract_skills_single(text, PARAMS):
    skills = skill_extraction_step(text, PARAMS)
    return skills

def process_batch(batch_data):
    batch, batch_id, PARAMS = batch_data
    print(f"Processing batch {batch_id} with {len(batch)} items...")
    time.sleep(1)
    results = []
    for i, text in enumerate(batch):
        print(f":  Processing item no.  {i} - {batch_id}")
        results.append(extract_skills_single(text, PARAMS))
    return (batch_id, results)

def extract_skills_batch(text_list, PARAMS, workers=4):
    if len(text_list) < workers:
        print("TOO MANY WORKERS FOR THIS NUMBER OF TEXT")
        exit()

    batch_size = (len(text_list) + workers - 1) // workers
    batches = [
        (text_list[i * batch_size : (i + 1) * batch_size], i, PARAMS)
        for i in range(workers)
    ]

    all_results = [None] * workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(process_batch, batch) for batch in batches]
        for future in concurrent.futures.as_completed(futures):
            batch_id, results = future.result()
            all_results[batch_id] = results

    return [item for sublist in all_results for item in sublist]

def estimate_extraction_costs(text, workers):
    if type(text) == str:
        text = [text]

    print(f"\nEstimate processing duration: {round(1 * (len(text) / workers), 3)}m")
    print(f"Estimate processing cost    : ${round(0.004 * len(text), 6)}\n")

job_postings_batches = [
    "Software Engineer needed to develop and maintain scalable backend services. Experience with Python and cloud platforms required.",
    "Marketing Intern wanted to assist with social media campaigns and content creation. Must be creative and detail-oriented.",
    "Data Analyst role open for candidates skilled in SQL, Excel, and data visualization tools like Power BI or Tableau.",
    "Hiring Administrative Assistant to manage scheduling, emails, and office logistics. Strong communication and organization skills required.",
    "UX Designer wanted to design user-friendly web interfaces. Proficiency in Figma and user research is a plus.",
    "Remote Customer Support Representative needed to handle inquiries and resolve issues via chat and email. Training provided.",
    "Project Manager sought to oversee product development. PMP certification and agile experience are preferred.",
    "Graphic Designer needed for brand assets, social media posts, and promotional materials. Adobe Creative Suite proficiency required.",
    "Looking for a Cybersecurity Specialist to monitor systems, conduct audits, and implement protective measures. Experience required."
]

job_posting_NC = "Description of Work If there are no qualified candidates remaining in the applicant pool who meet the minimum education and experience, or knowledge, skills and abilities required for the position then, an applicant who does not meet the minimum requirements may be considered for hire as a trainee. Salary for a trainee may be set lower than the classification salary range and recruitment range that is listed in the posting.  The salary is adjusted as the trainee obtains the additional education and experience to fully meet the position qualifications as outlined in the classification specification. The North Carolina Forest Service is a team of professionals who provide forest protection, emergency response, resource management and environmental education to the residents and landowners of North Carolina through a variety of programs.  The NC Forest Service provides services to the 100 counties in North Carolina. The Assistant County Ranger works with the County Ranger to provide services. Position requires: Assist with servicing landowner requests for forestry assistance Assist with programs to promote the importance of trees and tree care in the urban setting Provide and promote forestry education through interaction with forestry partners, schools, civic groups and school organizations such as Tree Farm, National Wild Turkey Federation, FFA and 4-H Promote the protection of the State’s natural resources through development of wildfire suppression planning Respond in times of emergency such as wildland fires and natural disasters Work hours are typically 8-5 M-F.  Extended times of readiness will involve evening, holiday, and/or weekend work.   Must be available after working hours during fire danger periods and times of emergency response. Overnight travel will be required. Residency requirements discussed at time of interview. Duty Station Location: 822 Fire Tower Road, Rose Hill, NC 28458 This position requires the successful completion of an employer provided Ranger Training. Official NC Forest Service uniform and a State-owned vehicle will be provided to support everyday job responsibilities. Click Here to Learn more about State Employee Benefits. The N.C. Department of Agriculture and Consumer Services provides services that promote and improve agriculture, agribusiness, and forests; protect consumers and businesses; and conserve farmland and natural resources for the prosperity of all North Carolinians.  The Department employs approximately 2,000 employees. Click Here to Watch this video to Learn How to Apply. Knowledge, Skills and Abilities / Competencies Knowledge of forest management, wildfire suppression or use of GPS/GIS software Excellent written and verbal communication skills Ability to organize and prioritize tasks to accomplish goals Must be self-motivated, a team player, and able to remain calm under stress Minimum Education and Experience Requirements You may qualify by an equivalent combination of education and experience, either through years of education or years of directly related experience, or a combination of both. Associate's degree in forest management or an environmental or natural science curriculum from an appropriately accredited institution; or High school or General Educational Development (GED) diploma and two years of related experience in providing forestry services; or an equivalent combination of training and experience. Necessary Special Qualification: Possession of a valid North Carolina driver's license required within 90 days of hire. Supplemental and Contact Information Any employment offer may be less than the maximum of the range due to salary equity with similarly situated employees or the selected candidate's related education and experience. Please follow the instructions to apply online. It is important that your application includes all your relevant education and experience. Text or attached resumes ARE NOT accepted as a substitution for a completed application. Applicants seeking veteran's/National Guard preference should submit a copy of their Form DD-214, NGB 23A (RPAS), DD256 or NGB 22. All Law Enforcement positions, aviation safety-sensitive positions, and positions requiring a Pilot's License or a Commercial Driver's License (CDL) shall be subject to pre-employment drug testing. All positions requiring a Commercial Driver's License shall also be subject to pre-employment DMV physicals. Selected applicants must obtain a U.S. Department of Transportation (USDOT) medical certificate prior to employment. If a CDL is listed as a preference and the selected applicant has a CDL at the time of hire, then the CDL will become a requirement for the position. * Note: When required, you must answer the question(s) for this position, or your application will be considered incomplete. * Questions regarding this posting?  Contact 919-707-3201."
# To summarize, this job requires a quilified forest ranger being able to operate GPS systems, have knowledge in forest management and wildfire suppression, communicate with emergency services,  and stay calm in stressful situations. 


if __name__ == "__main__":
    # Init client
    PARAMS["client"] = init_client()
    workers = 3
    text_list = job_postings_batches

    estimate_extraction_costs(text_list, workers)

    """With a single text"""
    # skills = extract_skills_single(job_posting_NC, PARAMS)
    # print(skills)

    """With a mutliple texts"""
    skills = extract_skills_batch(job_postings_batches, PARAMS, workers)
    print(skills)










# import json
# with open(r"C:\Users\artio\OneDrive\Desktop\4_AI_Skills\job_matching\NC_state_job_postings.json", "r") as file:
#     postings = json.load(file)

# all_NC_jobs = []
# for posting in postings:
#     one_string = ""
#     for string in posting["description"]:
#         one_string = one_string +  string.replace("\n", " ") + " "
    
#     all_NC_jobs.append(one_string)