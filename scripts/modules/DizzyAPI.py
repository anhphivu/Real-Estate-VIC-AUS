import os
import dotenv
import random
import time

class DizzyAPI:
    """Read all token from a .env file in the form of KEYx = _token_ where x is a number and _token_
    is the token. Below is the sumary of each methods and attribute, check each method for more info
    
    Method:
        __init__(): initiate the DizzyAPI object with path to .env file and the quota of the api
        reset_count(): reset the object to the initial state without rereading the file
        set_delay(): set the object delay between each request
        get_token(): return a valid token if possiple
        _get_request_interval_(): calculate the interval between each request in milisecond
        _delay_(): pause the function
        _token_is_valid_(): check validity of a token
        _update_validity_(): check for expired token from list of valid token
        
    Attribute:
        all_tokens: list of all token from
        quota: dictionary of quota for each token
        cost (float): the cost for 1 call of each key to be deduced from its quota
        valid_tokens: list of valid_token
        expired_token: list of token where its quota has been reach
        current_index: the index of the token to be return from valid_tokens
        total_request: the total number of time where get_token() has return a valid token
    """    
    
    def __init__(self, path, quota, num_token=20, rate=120, cost=1):
        """initiate the DizzyAPI object with path to secret key and quota

        Args:
            path (str): path to secrete key in .env
            quota (int | list): a list or a single number to set the quota for each key
            rate (int): the max number of request per minute. Default to 120
            num_token (int): the max number of token to check for in the input. Default to 20
            cost (float): the cost for 1 call of each key to be deduced from its quota
        """        
        # get all tokens from .env file
        dotenv.load_dotenv(path)
        self.where = path
        token_list = []
        for i in range(1, num_token + 1): 
            _token = os.environ.get(f'KEY{i}')
            if _token is not None and _token != "":
                token_list.append(_token)

        # set initial attribute
        self.all_tokens = token_list
        self.quota = {_token: quota for _token in token_list} if type(quota) == int else \
                            {token_list[i]: quota[i] for i in range(len(quota))}
        self.rate = rate
        self.cost = cost
        self.valid_tokens = token_list
        self.expired_tokens = []
        self.current_index = 0
        self.total_request = 0
        self.set_delay(const_delay=self._get_request_interval_(rpm=rate))
        return 
    
    def reset_count(self, quota, rate=120, cost=1):
        """Refresh the remaining quota count with new quota as well as total request and run time

        Args:
            quota (int): the new number of quota.
            rate (int): the max number of request per minute.  Default to 120
            cost (float): the cost for 1 call of each key to be deduced from its quota
        Returns:
            self: the refreshed DizzyAPI object.
        """        
        self.quota = {_token: quota for _token in self.all_tokens}
        
        self.rate = rate
        self.cost = cost
        self.valid_tokens = self.all_tokens
        self.expired_tokens = []
        self.current_index = 0
        self.total_request = 0
        self.set_delay(const_delay=self._get_request_interval_(rpm=rate))
        return self
    
    def _get_request_interval_(self, rpm=None, buffer=0):
        """Calculate the interval between each request base on the number of request per minute and 
            the current number of valid token

        Args:
            rpm (int | None, optional): the api's number of request per minute. If not provided then the
                                                       initial rate is used. Defaults to None.
            buffer (int, optional): abbitrary delay to be add. Defaults to 0.

        Returns:
            float: the interval between each request in milisecond
        """        
        num_tokens = len(self.valid_tokens)
        if rpm is None:
            rpm = self.rate
        interval = round(60 / (rpm * num_tokens) + buffer, 3)
        return interval 
    
    def set_delay(self, const_delay=0, lower=1, upper=500, random_delay=False):
        """set the range for the intended delay between each return of api keys
        
        Args:   
            const_delay (int, optional): delay is set to this if random_delay is False. Defaults to 0.
            lower (int, optional): lower bound of random delay. Defaults to 1.
            upper (int, optional): upper bound of random delay. Defaults to 500.
            random_delay (bool, optional): set to true to apply random delay between each call. 
                                                              But why???. Defaults to False.

        Returns:
            self: the modified DizzyAPI object
        """        
        self.delay_range = {'const_delay': const_delay,
                                       'rand_delay_lower_bound': lower, 
                                       'rand_delay_upper_delay_bound': upper}
        self.random_delay = random_delay
        return self
        
    def _delay_(self, pause=False):
        """Pause the program for sometime. To set the amount of time, use .set_delay()
            
        Args:
            pause (bool, optional): set to True to pause until Enter is pressed. Defaults to False.
        """         
        if pause: 
            input(f'Total request: {self.total_request}. Press <Enter> to continue')        
        if self.random_delay:
            lower = self.delay_range['rand_delay_lower_bound']
            upper = self.delay_range['rand_delay_upper_delay_bound']
            amount = random.randint(lower, upper) / 1000
        else:
            amount = self.delay_range['const_delay']
        time.sleep(amount)
        return 
    
    def _token_is_valid_(self, token=None):
        """Check if the current token is still usable, if a token is provided then check it instead

        Args:
            token (str, optional): _description_. Defaults to None.

        Returns:
            Bool: validity of the token
        """        
        if token is None:
            token = self.valid_tokens[self.current_index]
        return self.quota[token] > 0
    
    def _update_validity_(self):
        """Check if there is any valid token left and update the validity of each token in the list
            and reset request rate
            
        Returns:
            Bool: if there is still valid token left
        """        
        # valid list not empty -> update validity
        i = 0
        while i < len(self.valid_tokens):
            _token = self.valid_tokens[i]
            if self._token_is_valid_(token=_token):
                i += 1
                continue
            else:
                # move _token from valid list to expired list
                self.expired_tokens.append(self.valid_tokens.pop(i))
                if i <= self.current_index:
                    self.current_index -= 1
                    
        if len(self.valid_tokens) > 0:
            self.set_delay(self._get_request_interval_())
            return True
        
        # valid list empty 
        print('Out of quota')
        return False
        
    
    def get_token(self):
        """Get one of the avaiable token if there is one avaiable

        Returns:
            str | Boolean: the token or False if there is no valid token left
        """                  
        self._delay_()
        if self._update_validity_():
            token = self.valid_tokens[self.current_index]
            self.quota[token] -= self.cost
            self.current_index = (self.current_index + 1) % len(self.valid_tokens)
            self.total_request += 1
            return token
        return False
        