from django.urls import path
from .views import PortfolioListView, PortfolioDetailView, PortfolioCreateView, PortfolioUpdateView, PortfolioDeleteView
from . import views

urlpatterns = [    
	path('', PortfolioListView.as_view(), name='stocktracker-home'),
	path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
	path('portfolio/new/', PortfolioCreateView.as_view(), name='portfolio-create'),
	path('portfolio/<int:pk>/update/', PortfolioUpdateView.as_view(), name='portfolio-update'),
	path('portfolio/<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio-delete'),
	path('about/', views.about, name='stocktracker-about'),
	path('search/', views.SearchResultsView.as_view(), name='search_results'),
	path('stock/<str:slug>/', views.StockDetailView.as_view(), name='stock-detail'),
]
# Make unique path('stock/<str:ticker>'), will I think possible.
# def get_absolute_url(self): kwargs={'ticker': self.ticker}