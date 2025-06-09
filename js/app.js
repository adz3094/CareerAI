        let formData = {
            educationLevel: '',
            skills: [],
            interests: [],
            workPreferences: [],
            softSkills: []
        };

        // Form options data
        const formOptions = {
            skills: [
                // Technical Skills
                { value: 'programming', label: 'Programming/Coding', category: 'Technical' },
                { value: 'data_analysis', label: 'Data Analysis', category: 'Technical' },
                { value: 'web_development', label: 'Web Development', category: 'Technical' },
                { value: 'database_management', label: 'Database Management', category: 'Technical' },
                { value: 'cybersecurity', label: 'Cybersecurity', category: 'Technical' },
                { value: 'cloud_computing', label: 'Cloud Computing', category: 'Technical' },
                { value: 'ai_ml', label: 'AI/Machine Learning', category: 'Technical' },
                
                // Creative Skills
                { value: 'graphic_design', label: 'Graphic Design', category: 'Creative' },
                { value: 'video_editing', label: 'Video Editing', category: 'Creative' },
                { value: 'photography', label: 'Photography', category: 'Creative' },
                { value: 'writing', label: 'Creative Writing', category: 'Creative' },
                { value: 'ui_ux_design', label: 'UI/UX Design', category: 'Creative' },
                
                // Business Skills
                { value: 'project_management', label: 'Project Management', category: 'Business' },
                { value: 'marketing', label: 'Marketing', category: 'Business' },
                { value: 'sales', label: 'Sales', category: 'Business' },
                { value: 'accounting', label: 'Accounting/Finance', category: 'Business' },
                { value: 'business_analysis', label: 'Business Analysis', category: 'Business' },
                
                // Communication Skills
                { value: 'public_speaking', label: 'Public Speaking', category: 'Communication' },
                { value: 'technical_writing', label: 'Technical Writing', category: 'Communication' },
                { value: 'languages', label: 'Foreign Languages', category: 'Communication' },
                
                // Other Skills
                { value: 'research', label: 'Research', category: 'Other' },
                { value: 'teaching', label: 'Teaching/Training', category: 'Other' },
                { value: 'healthcare', label: 'Healthcare', category: 'Other' },
                { value: 'engineering', label: 'Engineering', category: 'Other' }
            ],
            
            interests: [
                { value: 'technology', label: 'Technology & Innovation' },
                { value: 'healthcare', label: 'Healthcare & Medicine' },
                { value: 'education', label: 'Education & Learning' },
                { value: 'arts_culture', label: 'Arts & Culture' },
                { value: 'business_finance', label: 'Business & Finance' },
                { value: 'environment', label: 'Environment & Sustainability' },
                { value: 'social_impact', label: 'Social Impact & Non-profit' },
                { value: 'sports_fitness', label: 'Sports & Fitness' },
                { value: 'travel_hospitality', label: 'Travel & Hospitality' },
                { value: 'food_culinary', label: 'Food & Culinary Arts' },
                { value: 'science_research', label: 'Science & Research' },
                { value: 'law_legal', label: 'Law & Legal Services' },
                { value: 'media_entertainment', label: 'Media & Entertainment' },
                { value: 'real_estate', label: 'Real Estate' },
                { value: 'manufacturing', label: 'Manufacturing & Industry' },
                { value: 'agriculture', label: 'Agriculture & Farming' },
                { value: 'government', label: 'Government & Public Service' },
                { value: 'consulting', label: 'Consulting & Advisory' }
            ],
            
            workPreferences: [
                { value: 'remote_work', label: 'Remote Work' },
                { value: 'flexible_hours', label: 'Flexible Hours' },
                { value: 'work_life_balance', label: 'Work-Life Balance' },
                { value: 'job_security', label: 'Job Security/Stability' },
                { value: 'high_salary', label: 'High Salary Potential' },
                { value: 'career_growth', label: 'Career Growth Opportunities' },
                { value: 'creative_freedom', label: 'Creative Freedom' },
                { value: 'team_collaboration', label: 'Team Collaboration' },
                { value: 'independent_work', label: 'Independent Work' },
                { value: 'travel_opportunities', label: 'Travel Opportunities' },
                { value: 'learning_development', label: 'Continuous Learning' },
                { value: 'leadership_roles', label: 'Leadership Opportunities' },
                { value: 'startup_environment', label: 'Startup Environment' },
                { value: 'corporate_structure', label: 'Corporate Structure' },
                { value: 'social_impact', label: 'Making Social Impact' },
                { value: 'innovation', label: 'Innovation & Cutting-edge Work' }
            ],
            
            softSkills: [
                { value: 'leadership', label: 'Leadership' },
                { value: 'communication', label: 'Communication' },
                { value: 'problem_solving', label: 'Problem Solving' },
                { value: 'creativity', label: 'Creativity' },
                { value: 'adaptability', label: 'Adaptability' },
                { value: 'teamwork', label: 'Teamwork' },
                { value: 'time_management', label: 'Time Management' },
                { value: 'critical_thinking', label: 'Critical Thinking' },
                { value: 'emotional_intelligence', label: 'Emotional Intelligence' },
                { value: 'attention_to_detail', label: 'Attention to Detail' },
                { value: 'initiative', label: 'Initiative' },
                { value: 'patience', label: 'Patience' },
                { value: 'negotiation', label: 'Negotiation' },
                { value: 'organization', label: 'Organization' },
                { value: 'empathy', label: 'Empathy' },
                { value: 'resilience', label: 'Resilience' },
                { value: 'analytical_thinking', label: 'Analytical Thinking' },
                { value: 'decision_making', label: 'Decision Making' }
            ]
        };

        // Initialize the form
        function initializeForm() {
            // Populate skills by category
            const skillsByCategory = {
                'Technical': [],
                'Creative': [],
                'Business': [],
                'Communication': [],
                'Other': []
            };

            formOptions.skills.forEach(skill => {
                skillsByCategory[skill.category].push(skill);
            });

            Object.entries(skillsByCategory).forEach(([category, skills]) => {
                const containerId = category.toLowerCase() + '-skills';
                const container = document.getElementById(containerId);
                
                skills.forEach(skill => {
                    const div = document.createElement('div');
                    div.className = 'checkbox-item';
                    div.innerHTML = `
                        <input type="checkbox" id="skill-${skill.value}" class="checkbox" value="${skill.value}" onchange="handleMultiSelect('skills', '${skill.value}')">
                        <label for="skill-${skill.value}" class="checkbox-label">${skill.label}</label>
                    `;
                    container.appendChild(div);
                });
            });

            // Populate interests
            const interestsContainer = document.getElementById('interests');
            formOptions.interests.forEach(interest => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="interest-${interest.value}" class="checkbox" value="${interest.value}" onchange="handleMultiSelect('interests', '${interest.value}')">
                    <label for="interest-${interest.value}" class="checkbox-label">${interest.label}</label>
                `;
                interestsContainer.appendChild(div);
            });

            // Populate work preferences
            const workPrefContainer = document.getElementById('work-preferences');
            formOptions.workPreferences.forEach(pref => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="workpref-${pref.value}" class="checkbox" value="${pref.value}" onchange="handleMultiSelect('workPreferences', '${pref.value}')">
                    <label for="workpref-${pref.value}" class="checkbox-label">${pref.label}</label>
                `;
                workPrefContainer.appendChild(div);
            });

            // Populate soft skills
            const softSkillsContainer = document.getElementById('soft-skills');
            formOptions.softSkills.forEach(skill => {
                const div = document.createElement('div');
                div.className = 'checkbox-item';
                div.innerHTML = `
                    <input type="checkbox" id="softskill-${skill.value}" class="checkbox" value="${skill.value}" onchange="handleMultiSelect('softSkills', '${skill.value}')">
                    <label for="softskill-${skill.value}" class="checkbox-label">${skill.label}</label>
                `;
                softSkillsContainer.appendChild(div);
            });

            // Add education level change handler
            document.getElementById('educationLevel').onchange = function(e) {
                formData.educationLevel = e.target.value;
                updateJsonDisplay();
            };
        }

        function handleMultiSelect(field, value) {
            if (formData[field].includes(value)) {
                formData[field] = formData[field].filter(item => item !== value);
            } else {
                formData[field].push(value);
            }
            updateJsonDisplay();
        }

        function updateJsonDisplay() {
            document.getElementById('json-output').textContent = JSON.stringify(formData, null, 2);
        }

        async function handleSubmit() {
        // Rebuild formData fresh from DOM elements
        const formData = {
            educationLevel: document.getElementById('educationLevel').value,
            skills: Array.from(document.querySelectorAll('input[id^="skill-"]:checked')).map(el => el.value),
            interests: Array.from(document.querySelectorAll('input[id^="interest-"]:checked')).map(el => el.value),
            workPreferences: Array.from(document.querySelectorAll('input[id^="workpref-"]:checked')).map(el => el.value),
            softSkills: Array.from(document.querySelectorAll('input[id^="softskill-"]:checked')).map(el => el.value)
        };

        console.log('Form Data:', formData);

        const response = await fetch("http://localhost:8000/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.recommendations && result.recommendations.length > 0) {
            localStorage.setItem('careerResults', JSON.stringify(result.recommendations));
            window.location.href = 'results.html';
        } else {
            alert("No recommendations were found. Please try again.");
        }
    }


        // Initialize the form when the page loads
        document.addEventListener('DOMContentLoaded', initializeForm);