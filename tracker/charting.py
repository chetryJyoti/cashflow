import plotly.express as px
from django.db.models import Sum
from tracker.models import Category

def plot_income_expenses_bar_chart(qs):
    x_vals = ["Income","Expenses"]

    total_income = qs.filter(type="income").aggregate(
        total = Sum("amount")
    )["total"]
    
    total_expenses = qs.filter(type="expense").aggregate(
        total = Sum("amount")
    )["total"]
    
    fig = px.bar(x=x_vals, y=[total_income,total_expenses])
    
    return fig

def plot_category_pie_chart(qs, type):
    """
    Creates a pie chart showing total amounts per category.

    Args:
        qs: Transaction queryset
        type: 'income' or 'expense' for chart title

    Returns:
        Plotly pie chart figure
    """
    # Get category totals with names in one query using select_related
    data = (
        qs.select_related('category')
        .values('category__name')  # Get category name directly
        .annotate(total=Sum('amount'))
        .order_by('-total')  # Order by highest amount first
    )

    # Extract names and amounts for the chart
    names = [item['category__name'] for item in data]
    values = [item['total'] for item in data]

    # Create pie chart
    fig = px.pie(values=values, names=names)

    # Set title
    title = f"Total {type} per category"
    fig.update_layout(title_text=title)

    return fig


# old way - not efficient too complex

# def plot_category_pie_chart(qs, type):
    """
    Creates a pie chart showing total amounts per category for either income or expenses.

    Args:
        qs (QuerySet): Filtered Transaction queryset (pre-filtered by user and transaction type)
        type (str): Either 'income' or 'expense' - used for chart title

    Returns:
        plotly.graph_objects.Figure: Pie chart figure ready for rendering
    """

    # Step 1: Group transactions by category and sum the amounts
    # This creates a dict-like result: [{'category': 1, 'total': 1500.00}, ...]
    count_per_category = (
        qs.order_by("category")           # Sort by category FK for consistent ordering
        .values("category")               # Group by category foreign key
        .annotate(total=Sum("amount"))    # Calculate sum of amounts per category
    )

    # Step 2: Extract just the category primary keys in the same order
    # Result: [1, 3, 5, ...] (category IDs that have transactions)
    category_pks = count_per_category.values_list("category", flat=True).order_by("category")

    # Step 3: Get the actual category names using the PKs
    # We order by pk to maintain the same sequence as our aggregated data
    # Result: ['Food', 'Transport', 'Salary', ...]
    categories = Category.objects.filter(
        pk__in=category_pks
    ).order_by("pk").values_list("name", flat=True)

    # Step 4: Extract the total amounts in the same order as categories
    # Result: [1500.00, 800.50, 3000.00, ...] (totals matching category order)
    total_amounts = count_per_category.order_by("category").values_list("total", flat=True)

    # Step 5: Create the pie chart with Plotly Express
    # values: The numerical data (total amounts)
    # names: The labels for each slice (category names)
    fig = px.pie(values=total_amounts, names=categories)

    # Step 6: Set appropriate title based on transaction type
    if type == 'income':
        fig.update_layout(title_text="Total income per category")
    else:
        fig.update_layout(title_text="Total expense per category")

    return fig