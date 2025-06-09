# ml_logic.py
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import re

def normalize(text: str) -> str:
        return re.sub(r'[^a-z0-9]', '_', text.lower())

class CareerRecommender:
    def __init__(self, careers_file_path: str = "careers.json"):
        """
        Initialize the Career Recommender with a careers dataset
        
        Args:
            careers_file_path: Path to the JSON file containing career data
        """
        self.careers_file_path = careers_file_path
        self.master_features = []
        self.career_vectors = []
        self.career_data = []
        
        # Define education hierarchy matching your HTML form
        self.education_hierarchy = {
            "high_school": 1,
            "some_college": 2,
            "associates": 3,
            "diploma": 3,  # Same level as associates
            "trade_school": 3,  # Same level as associates/diploma
            "professional_cert": 3,  # Same level as associates/diploma
            "bachelors": 4,
            "masters": 5,
            "doctorate": 6,
            "phd": 6,  # Same as doctorate
            "law_degree": 5  # Same level as masters (specialized degree)
        }
        
        # Load and process the career data
        self._load_career_data()
        self._create_master_features()
        self._create_career_vectors()
    
    def _load_career_data(self):
        """Load career data from JSON file"""
        try:
            with open(self.careers_file_path, 'r') as file:
                self.career_data = json.load(file)
            print(f"Loaded {len(self.career_data)} careers from {self.careers_file_path}")
        except FileNotFoundError:
            print(f"Warning: {self.careers_file_path} not found. Using sample data.")
            self.career_data = self._get_sample_career_data()

    def _get_sample_career_data(self):
        """Sample career data for testing purposes"""
        return [
            {
                "title": "Software Developer",
                "required_education": "bachelors",
                "skills": ["Programming/Coding", "Web Development", "Database Management"],
                "interests": ["Technology & Innovation"],
                "traits": ["Analytical Thinking", "Creativity", "Teamwork"]
            },
            {
                "title": "UX Designer",
                "required_education": "bachelors",
                "skills": ["UI/UX Design", "Graphic Design", "Research"],
                "interests": ["Arts & Culture", "Technology & Innovation"],
                "traits": ["Creativity", "Empathy", "Communication"]
            },
            {
                "title": "Data Scientist",
                "required_education": "masters",
                "skills": ["Data Analysis", "Programming/Coding", "AI/Machine Learning"],
                "interests": ["Technology & Innovation", "Science & Research"],
                "traits": ["Analytical Thinking", "Problem Solving", "Critical Thinking"]
            },
            {
                "title": "Legal Advisor",
                "required_education": "law_degree",
                "skills": ["Legal Research", "Legal Writing", "Case Analysis"],
                "interests": ["Law & Justice", "Problem Solving"],
                "traits": ["Analytical Thinking", "Communication", "Attention to Detail"]
            }
        ]
    
    def _create_master_features(self):
        """
        Create a master list of all unique features from the career dataset
        This includes skills, interests, and traits (matching your dataset structure)
        """
        all_features = set()
        
        for career in self.career_data:
            # Extract all features from each career (matching your JSON structure)
            if 'skills' in career:
                all_features.update([normalize(f) for f in career['skills']])
            if 'interests' in career:
                all_features.update([normalize(f) for f in career['interests']])
            if 'traits' in career:  # Updated to match your dataset
                all_features.update([normalize(f) for f in career['traits']])
        
        # Convert to sorted list for consistent ordering
        self.master_features = sorted(list(all_features))
        print(f"Created master feature list with {len(self.master_features)} features")
        return self.master_features
    
    def user_input_to_vector(self, user_input: Dict) -> np.ndarray:
        """
        Convert user input JSON to binary vector based on master features
        
        Args:
            user_input: Dictionary containing user's selections
                       Expected keys: skills, interests, workPreferences, softSkills
        
        Returns:
            Binary numpy array where 1 = feature selected, 0 = not selected
        """
        user_features = set()
        
        # Combine all user selections into one set (matching your form structure)
        for key in ['skills', 'interests', 'workPreferences', 'softSkills']:
            if key in user_input and user_input[key]:
                user_features.update([normalize(f) for f in user_input[key]])
        
        # Create binary vector
        vector = np.zeros(len(self.master_features))
        for i, feature in enumerate(self.master_features):
            if feature in user_features:
                vector[i] = 1
        
        return vector
    
    def _create_career_vectors(self):
        """Convert all career profiles to binary vectors"""
        self.career_vectors = []
        
        for career in self.career_data:
            # Combine all career features (matching your dataset structure)
            career_features = set()
            for key in ['skills', 'interests', 'traits']:  # Updated to match your dataset
                if key in career and career[key]:
                    career_features.update([normalize(f) for f in career[key]])
            
            # Create binary vector
            vector = np.zeros(len(self.master_features))
            for i, feature in enumerate(self.master_features):
                if feature in career_features:
                    vector[i] = 1
            
            self.career_vectors.append(vector)
        
        self.career_vectors = np.array(self.career_vectors)
        print(f"Created {len(self.career_vectors)} career vectors")
    
    def _get_education_score(self, user_level: str, required_level: str) -> float:
        """
        Calculate education compatibility score
        
        Args:
            user_level: User's education level
            required_level: Career's required education level
            
        Returns:
            Score between 0.0 and 1.0 (1.0 = perfect match or overqualified, 0.7 = underqualified)
        """
        user_score = self.education_hierarchy.get(user_level.lower(), 1)
        required_score = self.education_hierarchy.get(required_level.lower(), 1)
        
        if user_score >= required_score:
            # User meets or exceeds requirements
            return 1.0
        else:
            # User is underqualified - still possible but lower score
            return 0.7
    
    def get_recommendations(self, user_input: Dict, top_k: int = 5) -> List[Dict]:
        """
        Get top career recommendations for a user
        
        Args:
            user_input: User's form data as dictionary
            top_k: Number of top recommendations to return
        
        Returns:
            List of dictionaries containing career recommendations with similarity scores
        """
        # Convert user input to vector
        user_vector = self.user_input_to_vector(user_input)
        
        # Handle case where user vector is all zeros
        if np.sum(user_vector) == 0:
            print("Warning: User vector is empty (no selections made)")
            # Return top careers by education level if no skills/interests selected
            user_level = user_input.get("educationLevel", "high_school")
            suitable_careers = []
            for i, career in enumerate(self.career_data):
                education_score = self._get_education_score(user_level, career.get("required_education", "high_school"))
                if education_score >= 0.7:  # Include if education is reasonable match
                    suitable_careers.append({
                        "rank": len(suitable_careers) + 1,
                        "title": career["title"],
                        "similarity_score": education_score,
                        "career_details": career
                    })
            return suitable_careers[:top_k]
        
        # Calculate cosine similarity with all career vectors
        user_vector_2d = user_vector.reshape(1, -1)
        similarities = cosine_similarity(user_vector_2d, self.career_vectors)[0]
        
        # Apply education filtering and scoring
        user_level = user_input.get("educationLevel", "high_school")
        adjusted_scores = []
        
        for i, base_score in enumerate(similarities):
            required_level = self.career_data[i].get("required_education", "high_school")
            education_multiplier = self._get_education_score(user_level, required_level)
            
            # Combine similarity and education scores
            final_score = base_score * education_multiplier
            adjusted_scores.append(final_score)
        
        # Get top k recommendations
        adjusted_scores = np.array(adjusted_scores)
        top_indices = np.argsort(adjusted_scores)[-top_k:][::-1]  # Sort descending
        
        recommendations = []
        for i, idx in enumerate(top_indices):
            recommendations.append({
                "rank": i + 1,
                "title": self.career_data[idx]["title"],
                "similarity_score": round(float(adjusted_scores[idx]), 3),
                "base_similarity": round(float(similarities[idx]), 3),
                "education_compatibility": self._get_education_score(user_level, self.career_data[idx].get("required_education", "high_school")),
                "career_details": self.career_data[idx]
            })
        
        return recommendations
    
    def print_master_features(self):
        """Print all master features for debugging"""
        print("\nMaster Features:")
        for i, feature in enumerate(self.master_features):
            print(f"{i}: {feature}")
    
    def print_education_hierarchy(self):
        """Print education hierarchy for debugging"""
        print("\nEducation Hierarchy:")
        for level, score in sorted(self.education_hierarchy.items(), key=lambda x: x[1]):
            print(f"{level}: {score}")
    
    def get_feature_analysis(self, user_input: Dict) -> Dict:
        """
        Analyze which features the user selected for debugging
        
        Args:
            user_input: User's form data
            
        Returns:
            Dictionary with analysis information
        """
        user_vector = self.user_input_to_vector(user_input)
        selected_features = [self.master_features[i] for i in range(len(user_vector)) if user_vector[i] == 1]
        
        return {
            "total_features": len(self.master_features),
            "selected_features": selected_features,
            "selection_count": len(selected_features),
            "user_vector_sum": int(np.sum(user_vector)),
            "education_level": user_input.get("educationLevel", "not_specified")
        }
    
    def get_education_compatible_careers(self, education_level: str) -> List[str]:
        """
        Get all careers compatible with a given education level
        
        Args:
            education_level: User's education level
            
        Returns:
            List of career titles that are compatible
        """
        compatible_careers = []
        for career in self.career_data:
            if self._get_education_score(education_level, career.get("required_education", "high_school")) >= 0.7:
                compatible_careers.append(career["title"])
        
        return compatible_careers


# Example usage and testing
if __name__ == "__main__":
    # Initialize the recommender
    recommender = CareerRecommender()
    
    # Print education hierarchy
    recommender.print_education_hierarchy()
    
    # Print master features for reference
    recommender.print_master_features()
    
    # Test with different education levels
    test_cases = [
        {
            "name": "Law Student",
            "input": {
                "educationLevel": "law_degree",
                "skills": ["Legal Research", "Legal Writing"],
                "interests": ["Law & Justice"],
                "workPreferences": [],
                "softSkills": ["Analytical Thinking", "Communication"]
            }
        },
        {
            "name": "Tech Professional",
            "input": {
                "educationLevel": "bachelors",
                "skills": ["Programming/Coding", "Web Development"],
                "interests": ["Technology & Innovation"],
                "workPreferences": [],
                "softSkills": ["Problem Solving", "Creativity"]
            }
        },
        {
            "name": "High School Graduate",
            "input": {
                "educationLevel": "high_school",
                "skills": ["Graphic Design"],
                "interests": ["Arts & Culture"],
                "workPreferences": [],
                "softSkills": ["Creativity"]
            }
        }
    ]
    
    print("\n" + "="*50)
    print("TESTING THE RECOMMENDER")
    print("="*50)
    
    for test_case in test_cases:
        print(f"\n{'-'*20} {test_case['name']} {'-'*20}")
        
        # Analyze user input
        analysis = recommender.get_feature_analysis(test_case['input'])
        print(f"Education Level: {analysis['education_level']}")
        print(f"Selected {analysis['selection_count']} features: {analysis['selected_features']}")
        
        # Get compatible careers by education
        compatible = recommender.get_education_compatible_careers(test_case['input']['educationLevel'])
        print(f"Education-compatible careers: {len(compatible)} total")
        
        # Get recommendations
        recommendations = recommender.get_recommendations(test_case['input'], top_k=3)
        
        print(f"\nTop 3 Career Recommendations:")
        for rec in recommendations:
            print(f"{rec['rank']}. {rec['title']}")
            print(f"   Final Score: {rec['similarity_score']:.3f}")
            print(f"   Base Similarity: {rec['base_similarity']:.3f}")
            print(f"   Education Match: {rec['education_compatibility']:.1f}")
            print(f"   Required Education: {rec['career_details'].get('required_education', 'N/A')}")
            print()