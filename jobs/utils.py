from jobs.views import job
from users.models import Employee
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_emplyees(job_text):
    all_employees = Employee.objects.all()
    bios = [emp.bio for emp in all_employees]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([job_text] + bios)  

    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # threshold = 0.2

    sorted_employees = sorted(
    zip(all_employees, similarities),
    key=lambda x: x[1],
    reverse=True
    )

    employees_by_language = Employee.objects.filter(
        programming_languages__in=getattr(job, 'programming_languages', []).all() if hasattr(job, 'programming_languages') else []
    ).distinct()

    final_employees = list(set(list(sorted_employees) + list(employees_by_language)))
    return final_employees