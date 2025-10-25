# Algorithm Schema Overview

**Author:** Abdel YEZZA (Ph.D)

A non-technical guide to understanding the algorithms used in the TOPSIS Profile Selection System.

---

## 🎯 Main Goal

**Match the best profiles to activities based on their skills and requirements.**

---

## 📊 Applied Algorithms & Scenarios

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROFILE-ACTIVITY MATCHING                    │
│                   Three Complementary Approaches                │
└─────────────────────────────────────────────────────────────────┘
```

---

## **Scenario 1: Ranking Profiles for Each Activity**
### Using: Profile Assignment System (MCAP) + TOPSIS

```
INPUT:
┌─────────────┐         ┌──────────────────┐
│  Profiles   │         │   Activities     │
│             │         │                  │
│ • Dev1      │         │ • Backend Dev    │
│ • Dev2      │         │ • Frontend Dev   │
│ • Dev3      │         │ • Team Lead      │
│ • ...       │         │ • ...            │
└─────────────┘         └──────────────────┘
   AQUIRED                   REQUIRED
   -------                   --------
      │                          │
      │                          │
      │       ┌───────────┐      │
      └──────>│  Skills   │<─────┘
              │           │
              │ • Python  │
              │ • Java    │
              │ • SQL     │
              │ • ...     │
              └───────────┘

STEP 1: Profile Assignment System (MCAP)
┌────────────────────────────────────────────────────┐
│  Skill Transformation Based on Threshold           │
│                                                    │
│  For each activity requirement:                    │
│  • If skill level >= Threshold (e.g., 3.0)         │
│    → Mark as BENEFICIAL (higher is better)         │
│  • If skill level < Threshold                      │
│    → Mark as NON-BENEFICIAL (lower is acceptable)  │
│                                                    │
│  Example: Backend Dev needs Python=5, Leadership=2 │
│  With threshold=3.0:                               │
│  • Python (5≥3): BENEFICIAL → maximize             │
│  • Leadership (2<3): NON-BENEFICIAL → minimize     │
└────────────────────────────────────────────────────┘
            │
            ▼
STEP 2: TOPSIS Algorithm
┌───────────────────────────────────────────────────┐
│  Multi-Criteria Decision Analysis                 │
│                                                   │
│  1. Normalize profile skills (make comparable)    │
│  2. Apply weights (importance of each skill)      │
│  3. Find IDEAL profile (best in all skills)       │
│  4. Find WORST profile (worst in all skills)      │
│  5. Calculate how close each profile is to IDEAL  │
│                                                   │
│  Result: Proximity Score (0 to 1)                 │
│  • 1.0 = Perfect match                            │
│  • 0.0 = Worst match                              │
└───────────────────────────────────────────────────┘
                        │
                        ▼
OUTPUT: Ranked List for Each Activity
┌──────────────────────────────────────────────────┐
│  Backend Development:                            │
│  1. Dev10 (Score: 0.95) ⭐ Best match            │
│  2. Dev7  (Score: 0.87)                          │  
│  3. Dev1  (Score: 0.82)                          │
│  ...                                             │
│                                                  │
│  Frontend Development:                           │
│  1. Dev2  (Score: 0.91) ⭐ Best match            │ 
│  2. Dev5  (Score: 0.85)                          │ 
│  ...                                             │
└──────────────────────────────────────────────────┘
```

**Use Case:**
- You have multiple activities and want to know the best candidates for each
- You need to see all qualified profiles ranked by suitability
- Helps in decision-making when you have flexibility in assignments

---

## **Scenario 2: Optimal One-to-One Assignment**
### Using: MCAP + TOPSIS + Hungarian Method

```
INPUT: Same as Scenario 1
            │
            ▼
STEPS 1-2: Same as Scenario 1 (MCAP + TOPSIS)
┌────────────────────────────────────────────────────┐
│  Create Compatibility Matrix                       │
│                                                    │
│           Backend  Frontend  TeamLead              │
│  Dev1      0.82      0.91      0.65                │
│  Dev2      0.75      0.85      0.70                │
│  Dev3      0.90      0.60      0.88                │
│                                                    │
│  Each cell = TOPSIS proximity score                │
└────────────────────────────────────────────────────┘
            │
            ▼
STEP 3: Hungarian Algorithm (Optimal Assignment)
┌────────────────────────────────────────────────────┐
│  Find the BEST overall assignment                  │
│                                                    │
│  Constraint: Each profile → ONE activity           │
│             Each activity → ONE profile            │
│                                                    │
│  Goal: Maximize total satisfaction                 │
│                                                    │
│  Algorithm finds optimal pairing considering       │
│  all possibilities simultaneously                  │
└────────────────────────────────────────────────────┘
            │
            ▼
OUTPUT: Optimal Assignments
┌────────────────────────────────────────────────────┐
│  Optimal Assignments:                              │
│                                                    │
│  Dev1  →  Frontend Development  (0.91)             │
│  Dev2  →  Team Lead             (0.70)             │
│  Dev3  →  Backend Development   (0.90)             │
│                                                    │
│  Total Score: 2.51 (best possible combination)     │
└────────────────────────────────────────────────────┘
```

**Use Case:**
- You need to assign exactly ONE profile to each activity
- No profile can be assigned to multiple activities
- You want the globally optimal solution, not just individual bests
- Example: Assigning team members to project roles

---

## 🔄 Key Differences Between Scenarios

| Aspect | Scenario 1 (Ranking) | Scenario 2 (Optimal Assignment) |
|--------|---------------------|--------------------------------|
| **Output** | Ranked list per activity | One-to-one assignments |
| **Flexibility** | Multiple candidates per activity | One profile per activity |
| **Optimization** | Individual activity level | Global level |
| **Algorithms** | MCAP + TOPSIS | MCAP + TOPSIS + Hungarian |
| **When to Use** | Exploring options | Final assignments |

---

## 🧩 How the Algorithms Complement Each Other

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   MCAP (Profile Assignment System)                           │
│   • Transforms requirements based on threshold               │
│   • Identifies what matters most for each activity           │
│   • Provides context for evaluation                          │
│                                                              │
│                        ↓                                     │
│                                                              │
│   TOPSIS (Multi-Criteria Decision)                           │
│   • Evaluates profiles against ideal solution                │
│   • Generates compatibility scores                           │
│   • Ranks profiles for each activity                         │
│                                                              │
│                        ↓                                     │
│                                                              │
│   HUNGARIAN (Optional - For Optimal Assignment)              │
│   • Uses TOPSIS scores as input                              │
│   • Finds globally optimal assignments                       │
│   • Ensures no conflicts (1 profile = 1 activity)            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📈 Real-World Example

### Context:
A company has 5 developers and 5 projects to assign.

### Scenario 1 Approach (Ranking):
```
Mobile App Project:
1. Alice   (0.95) ⭐
2. Bob     (0.88)
3. Charlie (0.75)

Web Platform Project:
1. Bob     (0.92) ⭐
2. Alice   (0.85)
3. Dave    (0.78)
```
**Result:** You see all options and can make informed decisions.

### Scenario 2 Approach (Optimal Assignment):
```
After considering ALL projects and developers together:

Alice   → Mobile App Project      (0.95)
Bob     → Web Platform Project    (0.92)
Charlie → Backend Service         (0.88)
Dave    → DevOps Infrastructure   (0.90)
Eve     → Data Pipeline           (0.87)

Total satisfaction: 4.52
```
**Result:** Best overall combination, no overlaps.

---

## 🎓 Summary

1. **MCAP** = Smart way to understand what each activity really needs
2. **TOPSIS** = Scientific method to score and rank profiles
3. **Hungarian** = Mathematical optimization for perfect assignments

**Together they provide:**
- **Flexibility** (Scenario 1): See all options
- **Optimality** (Scenario 2): Get the best overall solution

---

## 📚 References

- **Profile Assignment System (MCAP)**: [LinkedIn Article](https://www.linkedin.com/posts/abdel-yezza-consultant_profiles-assignment-github-project-activity-7299685203168415744-7UGb)
- **TOPSIS Algorithm**: [LinkedIn Article](https://www.linkedin.com/posts/abdel-yezza-consultant_algorithme-topsis-et-ses-variantes-en-python-activity-7384268427382870017-KduR)
- **Hungarian Algorithm**: For optimal assignment problems (see HUNGARIAN_METHOD documentation)

---

**Author:** Abdel YEZZA (Ph.D)
**Version:** 1.0.0
**Last Updated:** 2025
