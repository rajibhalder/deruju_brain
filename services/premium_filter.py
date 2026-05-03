LOW_VALUE_WORDS = {
# celebrity / royal
"celebrity",
"celeb",
"famous",
"royal",
"royal family",
"king",
"queen",
"prince",
"princess",
"duke",
"duchess",
"meghan",
"harry",
"charles",
"kate middleton",

# entertainment
"movie",
"film",
"cinema",
"actor",
"actors",
"actress",
"actresses",
"director",
"producer",
"box office",
"trailer",
"netflix",
"bollywood",
"hollywood",
"music video",

# gossip / lifestyle
"dating",
"marriage",
"wedding",
"divorce",
"relationship",
"fashion",
"style",
"viral photo",
"instagram",

# sports noise
"ipl",
"cricket match",
"football match",
"goal",
"tournament result",
"celeb match"
}

HIGH_VALUE_WORDS = {
# macro economy
"economy",
"economic",
"gdp",
"inflation",
"deflation",
"recession",
"growth",
"unemployment",
"interest rate",
"rbi",

# markets
"market",
"stock",
"equity",
"sensex",
"nifty",
"banking",
"bond",
"commodity",
"earnings",

# policy / politics
"policy",
"regulation",
"bill",
"law",
"governance",
"election",
"parliament",
"cabinet",
"budget",
"tax",

# geopolitics / security
"war",
"conflict",
"military",
"missile",
"border",
"terror",
"security",
"sanction",
"diplomacy",

# climate / disaster
"climate",
"heatwave",
"storm",
"cyclone",
"earthquake",
"flood",
"rainfall",
"wildfire",
"disaster",

# infrastructure / civic
"bridge collapse",
"fire safety",
"railway",
"airport",
"power grid",
"water crisis",

# technology
"technology",
"ai",
"artificial intelligence",
"chip",
"semiconductor",
"cybersecurity",
"cloud",
"robotics",
"automation",

# health
"disease",
"virus",
"outbreak",
"vaccine",
"hospital",
"public health",

# education / jobs
"education",
"exam",
"hiring",
"job market",
"skill",
"career"
}


def score_text(text: str, words: set):
	return sum(
	1 for w in words
	if w in text
	)

def is_premium(signal):
	text = (
	signal.title.lower()
	+ " "
	+ signal.why_it_matters.lower()
	)


	high_score = score_text(
		text,
		HIGH_VALUE_WORDS
	)

	low_score = score_text(
		text,
		LOW_VALUE_WORDS
	)

	if high_score >= 2:
		return True

	if low_score >= 2 and high_score == 0:
		return False

	if signal.india_relevance >= 70:
		return True

	if signal.rank_score >= 68:
		return True

	return False
