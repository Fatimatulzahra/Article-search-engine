from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)

    def test_keyword_to_titles(self):
        metadata1 = [['Les Cousins (music club)', 'Mack Johnson', 1187072433, 4926, ['les', 'cousins', 'was', 'and', 'club', 'the', 'john']],['Human computer', 'Bearcat', 1248275178, 4750, ['the', 'computer', 'from', 'first', 'one', 'who', 'mathematical', 'calculations', 'computers', 'human', 'often', 'women', 'were', 'used', 'and', 'work', 'was', 'that', 'this', 'also', 'with', 'for', 'computing', 'tables', 'project', 'his', 'had', 'worked', 'data', 'harvard', 'committee', 'pearson', 'humans', 'world', 'war']],['Aube (musician)', 'Mack Johnson', 1145410600, 3152, ['akifumi', 'his', 'aube', 'was', 'and', 'the', 'with']]]
        metadata2 = [['Kevin Cadogan', 'Mr Jake', 1144136316, 3917, ['cadogan', 'record', 'and', 'the', 'band', 'third', 'eye', 'blind', 'with', 'from', 'their', 'album', 'his', 'jenkins', 'recording', 'elektra', 'records', 'was', 'for', 'california', 'two', 'music', 'that', 'have', 'were']], ['Endogenous cannabinoid', 'Pegship', 1168971903, 26, []]]
        metadata3 = [['Endogenous cannabinoid', 'Pegship', 1168971903, 26, []]]
        expected_metadata1 = {'les': ['Les Cousins (music club)'], 'cousins': ['Les Cousins (music club)'], 'was': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'and': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'club': ['Les Cousins (music club)'], 'the': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'john': ['Les Cousins (music club)'], 'computer': ['Human computer'], 'from': ['Human computer'], 'first': ['Human computer'], 'one': ['Human computer'], 'who': ['Human computer'], 'mathematical': ['Human computer'], 'calculations': ['Human computer'], 'computers': ['Human computer'], 'human': ['Human computer'], 'often': ['Human computer'], 'women': ['Human computer'], 'were': ['Human computer'], 'used': ['Human computer'], 'work': ['Human computer'], 'that': ['Human computer'], 'this': ['Human computer'], 'also': ['Human computer'], 'with': ['Human computer', 'Aube (musician)'], 'for': ['Human computer'], 'computing': ['Human computer'], 'tables': ['Human computer'], 'project': ['Human computer'], 'his': ['Human computer', 'Aube (musician)'], 'had': ['Human computer'], 'worked': ['Human computer'], 'data': ['Human computer'], 'harvard': ['Human computer'], 'committee': ['Human computer'], 'pearson': ['Human computer'], 'humans': ['Human computer'], 'world': ['Human computer'], 'war': ['Human computer'], 'akifumi': ['Aube (musician)'], 'aube': ['Aube (musician)']}
        expected_metadata2 = {'cadogan': ['Kevin Cadogan'], 'record': ['Kevin Cadogan'], 'and': ['Kevin Cadogan'], 'the': ['Kevin Cadogan'], 'band': ['Kevin Cadogan'], 'third': ['Kevin Cadogan'], 'eye': ['Kevin Cadogan'], 'blind': ['Kevin Cadogan'], 'with': ['Kevin Cadogan'], 'from': ['Kevin Cadogan'], 'their': ['Kevin Cadogan'], 'album': ['Kevin Cadogan'], 'his': ['Kevin Cadogan'], 'jenkins': ['Kevin Cadogan'], 'recording': ['Kevin Cadogan'], 'elektra': ['Kevin Cadogan'], 'records': ['Kevin Cadogan'], 'was': ['Kevin Cadogan'], 'for': ['Kevin Cadogan'], 'california': ['Kevin Cadogan'], 'two': ['Kevin Cadogan'], 'music': ['Kevin Cadogan'], 'that': ['Kevin Cadogan'], 'have': ['Kevin Cadogan'], 'were': ['Kevin Cadogan']}
        self.assertEqual(keyword_to_titles(metadata1), expected_metadata1)
        self.assertEqual(keyword_to_titles(metadata2), expected_metadata2)
        self.assertEqual(keyword_to_titles([]), {})
        self.assertEqual(keyword_to_titles(metadata3), {})


    def test_title_to_info(self):
        metadata1 = [['Kevin Cadogan', 'Mr Jake', 1144136316, 3917, ['cadogan', 'record', 'and', 'the', 'band', 'third', 'eye', 'blind', 'with', 'from', 'their', 'album', 'his', 'jenkins', 'recording', 'elektra', 'records', 'was', 'for', 'california', 'two', 'music', 'that', 'have', 'were']], ['Endogenous cannabinoid', 'Pegship', 1168971903, 26, []]]
        metadata2 = [['Les Cousins (music club)', 'Mack Johnson', 1187072433, 4926, ['les', 'cousins', 'was', 'and', 'club', 'the', 'john']],['Human computer', 'Bearcat', 1248275178, 4750, ['the', 'computer', 'from', 'first', 'one', 'who', 'mathematical', 'calculations', 'computers', 'human', 'often', 'women', 'were', 'used', 'and', 'work', 'was', 'that', 'this', 'also', 'with', 'for', 'computing', 'tables', 'project', 'his', 'had', 'worked', 'data', 'harvard', 'committee', 'pearson', 'humans', 'world', 'war']],['Aube (musician)', 'Mack Johnson', 1145410600, 3152, ['akifumi', 'his', 'aube', 'was', 'and', 'the', 'with']]]
        expected_metadata1 = {'Kevin Cadogan': {'author': 'Mr Jake', 'timestamp': 1144136316, 'length': 3917}, 'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}}
        expected_metadata2 = {'Les Cousins (music club)': {'author': 'Mack Johnson', 'timestamp': 1187072433, 'length': 4926}, 'Human computer': {'author': 'Bearcat', 'timestamp': 1248275178, 'length': 4750}, 'Aube (musician)': {'author': 'Mack Johnson', 'timestamp': 1145410600, 'length': 3152}}
        self.assertEqual(title_to_info(metadata1), expected_metadata1)
        self.assertEqual(title_to_info(metadata2), expected_metadata2)
        self.assertEqual(title_to_info([]), {})

    def test_search(self):
        keyword_to_titles_1 = {'les': ['Les Cousins (music club)'], 'cousins': ['Les Cousins (music club)'], 'was': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'and': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'club': ['Les Cousins (music club)'], 'the': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'john': ['Les Cousins (music club)'], 'computer': ['Human computer'], 'from': ['Human computer'], 'first': ['Human computer'], 'one': ['Human computer'], 'who': ['Human computer'], 'mathematical': ['Human computer'], 'calculations': ['Human computer'], 'computers': ['Human computer'], 'human': ['Human computer'], 'often': ['Human computer'], 'women': ['Human computer'], 'were': ['Human computer'], 'used': ['Human computer'], 'work': ['Human computer'], 'that': ['Human computer'], 'this': ['Human computer'], 'also': ['Human computer'], 'with': ['Human computer', 'Aube (musician)'], 'for': ['Human computer'], 'computing': ['Human computer'], 'tables': ['Human computer'], 'project': ['Human computer'], 'his': ['Human computer', 'Aube (musician)'], 'had': ['Human computer'], 'worked': ['Human computer'], 'data': ['Human computer'], 'harvard': ['Human computer'], 'committee': ['Human computer'], 'pearson': ['Human computer'], 'humans': ['Human computer'], 'world': ['Human computer'], 'war': ['Human computer'], 'akifumi': ['Aube (musician)'], 'aube': ['Aube (musician)']}
        keyword_to_titles_2 = {'edogawa': ['Edogawa, Tokyo'], 'the': ['Edogawa, Tokyo', 'Kevin Cadogan', '2007 Bulldogs RLFC season'], 'with': ['Edogawa, Tokyo', 'Kevin Cadogan', '2007 Bulldogs RLFC season'], 'and': ['Edogawa, Tokyo', 'Kevin Cadogan', '2007 Bulldogs RLFC season'], 'koiwa': ['Edogawa, Tokyo'], 'kasai': ['Edogawa, Tokyo'], 'player': ['Edogawa, Tokyo'], 'high': ['Edogawa, Tokyo'], 'school': ['Edogawa, Tokyo'], 'cadogan': ['Kevin Cadogan'], 'record': ['Kevin Cadogan'], 'band': ['Kevin Cadogan'], 'third': ['Kevin Cadogan'], 'eye': ['Kevin Cadogan'], 'blind': ['Kevin Cadogan'], 'from': ['Kevin Cadogan', '2007 Bulldogs RLFC season'], 'their': ['Kevin Cadogan', '2007 Bulldogs RLFC season'], 'album': ['Kevin Cadogan'], 'his': ['Kevin Cadogan'], 'jenkins': ['Kevin Cadogan'], 'recording': ['Kevin Cadogan'], 'elektra': ['Kevin Cadogan'], 'records': ['Kevin Cadogan'], 'was': ['Kevin Cadogan', '2007 Bulldogs RLFC season'], 'for': ['Kevin Cadogan', '2007 Bulldogs RLFC season'], 'california': ['Kevin Cadogan'], 'two': ['Kevin Cadogan'], 'music': ['Kevin Cadogan'], 'that': ['Kevin Cadogan'], 'have': ['Kevin Cadogan'], 'were': ['Kevin Cadogan'], '2007': ['2007 Bulldogs RLFC season'], 'bulldogs': ['2007 Bulldogs RLFC season'], 'season': ['2007 Bulldogs RLFC season'], 'telstra': ['2007 Bulldogs RLFC season'], 'against': ['2007 Bulldogs RLFC season'], 'stadium': ['2007 Bulldogs RLFC season'], 'game': ['2007 Bulldogs RLFC season'], 'down': ['2007 Bulldogs RLFC season'], 'one': ['2007 Bulldogs RLFC season'], 'comeback': ['2007 Bulldogs RLFC season'], 'saw': ['2007 Bulldogs RLFC season'], 'week': ['2007 Bulldogs RLFC season'], 'first': ['2007 Bulldogs RLFC season'], 'win': ['2007 Bulldogs RLFC season'], 'front': ['2007 Bulldogs RLFC season'], 'round': ['2007 Bulldogs RLFC season'], 'match': ['2007 Bulldogs RLFC season'], 'points': ['2007 Bulldogs RLFC season'], 'dogs': ['2007 Bulldogs RLFC season'], 'another': ['2007 Bulldogs RLFC season'], 'top': ['2007 Bulldogs RLFC season'], 'publishing': ['2007 Bulldogs RLFC season'], 'isbn': ['2007 Bulldogs RLFC season'], 'rugby': ['2007 Bulldogs RLFC season'], 'league': ['2007 Bulldogs RLFC season']}
        self.assertEqual(search('music', keyword_to_titles_1), [])
        self.assertEqual(search('was', keyword_to_titles_1), ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'])
        self.assertEqual(search('the', keyword_to_titles_2), ['Edogawa, Tokyo', 'Kevin Cadogan', '2007 Bulldogs RLFC season'])


    def test_article_length(self):
        article_titles_1 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music']
        title_to_info_1 = {'Kevin Cadogan': {'author': 'Mr Jake', 'timestamp': 1144136316, 'length': 3917}, 'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}, 'Noise (music)': {'author': 'jack johnson', 'timestamp': 1194207604, 'length': 15641}}
        self.assertEqual(article_length(5000, article_titles_1, title_to_info_1), ['Kevin Cadogan'])
        self.assertEqual(article_length(2000, article_titles_1, title_to_info_1), [])
        self.assertEqual(article_length(16000, article_titles_1, title_to_info_1), ['Noise (music)', 'Kevin Cadogan'])
        
        
    def test_key_by_author(self):
        article_titles_1 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music']
        title_to_info_1 = {'Kevin Cadogan': {'author': 'Mr Jake', 'timestamp': 1144136316, 'length': 3917}, 'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}}
        title_to_info_2 = {'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}}
        self.assertEqual(key_by_author(article_titles_1, title_to_info_1), {'Mr Jake': ['Kevin Cadogan']})
        self.assertEqual(key_by_author(article_titles_1, title_to_info_2), {})
        self.assertEqual(key_by_author([], title_to_info_2), {})

    def test_filter_to_author(self):
        article_titles_1 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music']
        title_to_info_1 = {'Kevin Cadogan': {'author': 'Mr Jake', 'timestamp': 1144136316, 'length': 3917}, 'Endogenous cannabinoid': {'author': 'Pegship', 'timestamp': 1168971903, 'length': 26}}
        self.assertEqual(filter_to_author('Mr Jake', article_titles_1, title_to_info_1), ['Kevin Cadogan'])
        self.assertEqual(filter_to_author('Fatimah', article_titles_1, title_to_info_1), [])
        self.assertEqual(filter_to_author('mr jake', article_titles_1, title_to_info_1), [])

    def test_filter_out(self):
        article_titles_1 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music']
        article_titles_2 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music', 'Aube (musician)']
 
        keyword_to_titles_1  = {'les': ['Les Cousins (music club)'], 'cousins': ['Les Cousins (music club)'], 'was': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'and': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'club': ['Les Cousins (music club)'], 'the': ['Les Cousins (music club)', 'Human computer', 'Aube (musician)'], 'john': ['Les Cousins (music club)'], 'computer': ['Human computer'], 'from': ['Human computer'], 'first': ['Human computer'], 'one': ['Human computer'], 'who': ['Human computer'], 'mathematical': ['Human computer'], 'calculations': ['Human computer'], 'computers': ['Human computer'], 'human': ['Human computer'], 'often': ['Human computer'], 'women': ['Human computer'], 'were': ['Human computer'], 'used': ['Human computer'], 'work': ['Human computer'], 'that': ['Human computer'], 'this': ['Human computer'], 'also': ['Human computer'], 'with': ['Human computer', 'Aube (musician)'], 'for': ['Human computer'], 'computing': ['Human computer'], 'tables': ['Human computer'], 'project': ['Human computer'], 'his': ['Human computer', 'Aube (musician)'], 'had': ['Human computer'], 'worked': ['Human computer'], 'data': ['Human computer'], 'harvard': ['Human computer'], 'committee': ['Human computer'], 'pearson': ['Human computer'], 'humans': ['Human computer'], 'world': ['Human computer'], 'war': ['Human computer'], 'akifumi': ['Aube (musician)'], 'aube': ['Aube (musician)']}
        expected_filter_out_1 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music']
        expected_filter_out_2 = ['List of Canadian musicians', 'French pop music', 'Noise (music)', '1922 in music', '1986 in music', 'Kevin Cadogan', '2009 in music', 'Rock music', 'Lights (musician)', 'Tim Arnold (musician)', 'Old-time music', 'Arabic music', 'Joe Becker (musician)', 'Richard Wright (musician)', 'Voice classification in non-classical music', '1936 in music', '1962 in country music', 'List of dystopian music, TV programs, and games', 'Steve Perry (musician)', 'David Gray (musician)', 'Alex Turner (musician)', 'List of gospel musicians', 'Indian classical music', '1996 in music', 'Traditional Thai musical instruments', '2006 in music', 'Tony Kaye (musician)', 'Texture (music)', '2007 in music', '2008 in music']
        self.assertEqual(filter_out('les', article_titles_1, keyword_to_titles_1), expected_filter_out_1)
        self.assertEqual(filter_out('akifumi', article_titles_2, keyword_to_titles_1), expected_filter_out_1)
        self.assertEqual(filter_out('egg', article_titles_1, keyword_to_titles_1), expected_filter_out_2)

    def test_articles_from_year(self):
        article_titles_1 = ['Black dog (ghost)', 'Mexican dog-faced bat', 'Dalmatian (dog)', 'Guide dog', 'Sun dog']
        title_to_info_1 = {'Guide dog': {'author': 'Jack Johnson', 'timestamp': 1165601603, 'length': 7339}, 'Dalmatian (dog)': {'author': 'Mr Jake', 'timestamp': 1207793294, 'length': 26582}, '1936 in music': {'author': 'RussBot', 'timestamp': 1243745950, 'length': 23417}}
        self.assertEqual(articles_from_year(2008, article_titles_1, title_to_info_1), ['Dalmatian (dog)'])
        self.assertEqual(articles_from_year(2007, article_titles_1, title_to_info_1), [])
        self.assertEqual(articles_from_year(2002, article_titles_1, title_to_info_1), [])


    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"
        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_article_length_integration(self, input_mock):
        keyword = 'music'
        advanced_option = 1
        advanced_response = 5000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Kevin Cadogan', 'Tim Arnold (musician)', 'List of gospel musicians', 'Texture (music)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_key_by_author_integration(self, input_mock):
        keyword = 'dog'
        advanced_option = 2
        # advanced_response = 5000
        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: {'Pegship': ['Black dog (ghost)'], 'Mack Johnson': ['Mexican dog-faced bat'], 'Mr Jake': ['Dalmatian (dog)', 'Sun dog'], 'Jack Johnson': ['Guide dog']}\n"
        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_to_author_integration(self, input_mock):
        keyword = 'dog'
        advanced_option = 3
        advanced_response = 'Pegship'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Black dog (ghost)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_filter_out_integration(self, input_mock):
        keyword = 'canada'
        advanced_option = 4
        advanced_response = 'music'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Will Johnson (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_none_integration(self, input_mock):
        keyword = 'cat'
        advanced_option = 6

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + "\n\nHere are your articles: ['Covariance and contravariance (computer science)']\n"

        self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
