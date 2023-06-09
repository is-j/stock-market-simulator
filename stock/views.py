import datetime, os, requests
from django.http import HttpResponse
from .models import Stock, Transaction, User, Portfolio
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
import plotly.graph_objs as go
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import TransactionForm, UserCreationForm, UserRegistrationForm, PortfolioForm
#Stock Detail View: This view provides detailed information about 
# a specific stock, including its current price, description, 
# and any other relevant data.
API_KEY = os.environ.get('API_KEY')

def index(request):
    return HttpResponse("This is the stock index")




import json

import plotly.graph_objs as go
from plotly.offline import plot
from django.shortcuts import render

def stock_list(request):
    stocks = Stock.objects.all()

    # Retrieve stock data for the graph
    dates = [stock.date for stock in stocks]
    close_prices = [stock.close_price for stock in stocks]
    open_prices = [stock.open_price for stock in stocks]
    high_prices = [stock.high_price for stock in stocks]
    low_prices = [stock.high_price for stock in stocks]

    # Create a line plot using Plotly
    trace = go.Candlestick(
        x=dates,
        open=open_prices,
        high=high_prices,
        low=low_prices,
        close=close_prices,
    )
    data = [trace]
    layout = go.Layout(
        title='Stock Market Data',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
    )
    fig = go.Figure(data=data, layout=layout)

    # Generate the HTML for the graph
    plot_div = plot(fig, output_type='div')

    return render(request, 'stock/stock_list.html', {'stocks': stocks, 'plot_html': plot_div})

def stock_detail(request):
    if request.method == 'POST':
        print(request.POST)
        symbol = request.POST['symbol']  # Symbol of the stock to import
        start_date = request.POST['start_date']  # Start date for data import
        end_date = request.POST['end_date']  # End date for data import
        api_key = os.environ.get('API_KEY')  # Replace with your Polygon.io API key

        # Make API request to Polygon.io
        url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={api_key}'
        response = requests.get(url)
        data = response.json()

        results = data['results']

        # Process and save data to the database
        for result in results:
            timestamp = result['t']
            date = datetime.datetime.fromtimestamp(timestamp / 1000).date()
            open_price = result['o']
            high_price = result['h']
            low_price = result['l']
            close_price = result['c']
            volume = result['v']

            stock = Stock(
                symbol=symbol,
                date = date,
                end_date = end_date, 
                start_date = start_date,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=volume
            )
            stock.save()

        return HttpResponse("Data imported successfully.") #Data

    return render(request, 'stock/stock_detail.html')


@login_required
def create_simulated_account(request):
    # Check if the user already has a simulated account
    if request.user.simulated_account:
        messages.warning(request, "You already have a simulated account.")
        return redirect('dashboard')

    # Create a simulated portfolio for the user
    Portfolio.objects.create(user=request.user, name="Simulated Portfolio")

    # Set the simulated_account field to True for the user
    request.user.simulated_account = True
    request.user.save()

    messages.success(request, "Simulated account created successfully.")
    return redirect('dashboard')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save(commit=False)

            # Set the simulated_account field to True for the new user
            user.simulated_account = True
            user.save()

            # Create a simulated portfolio for the new user
            Portfolio.objects.create(user=user, name="Simulated Portfolio")

            messages.success(request, "Simulated account created successfully. You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'stock/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'stock/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    portfolios = Portfolio.objects.filter(user=user)
    transactions = Transaction.objects.filter(user=user)

    context = {
        'user': user,
        'portfolios': portfolios,
        'transactions': transactions,
    }

    return render(request, 'stock/dashboard.html', context)



def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'stock/transaction_list.html', {'transactions': transactions})


def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'stock/create_transaction.html', {'form': form})


def portfolio_list(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, 'stock/portfolio_list.html', {'portfolios': portfolios})

def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    return render(request, 'stock/portfolio_detail.html', {'portfolio': portfolio})

def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect('portfolio_list')
    else:
        form = PortfolioForm()
    return render(request, 'stock/create_portfolio.html', {'form': form})

def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    if request.method == 'POST':
        portfolio.delete()
        return redirect('portfolio_list')
    return render(request, 'stock/delete_portfolio.html', {'portfolio': portfolio})


