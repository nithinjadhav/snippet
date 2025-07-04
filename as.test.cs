using Xunit;
using Moq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.AspNetCore.Http;
using AccountsApi.Middleware;
using AccountsApi.Services;
using AccountsApi.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

public class AccountSecurityAttributeTests
{
    private AccountSecurityAttribute CreateAttributeWithService(IAccountService service)
    {
        var attr = new AccountSecurityAttribute();
        return attr;
    }

    private ActionExecutingContext CreateContext(string path, string customerIdHeader)
    {
        var httpContext = new DefaultHttpContext();
        httpContext.Request.Path = path;
        if (customerIdHeader != null)
            httpContext.Request.Headers["X-Customer-Id"] = customerIdHeader;
        var actionContext = new ActionContext(httpContext, new Microsoft.AspNetCore.Routing.RouteData(), new Microsoft.AspNetCore.Mvc.Abstractions.ActionDescriptor());
        return new ActionExecutingContext(actionContext, new List<IFilterMetadata>(), new Dictionary<string, object>(), null);
    }

    [Fact]
    public async Task Returns_Forbidden_If_AccountId_Missing()
    {
        var mockService = new Mock<IAccountService>();
        var attr = CreateAttributeWithService(mockService.Object);
        var context = CreateContext("/api/accounts/", "100");
        var executed = false;
        await attr.OnActionExecutionAsync(context, () => { executed = true; return Task.FromResult<ActionExecutedContext>(null); });
        Assert.IsType<ObjectResult>(context.Result);
        var result = context.Result as ObjectResult;
        Assert.Equal(StatusCodes.Status403Forbidden, result.StatusCode);
    }

    [Fact]
    public async Task Returns_Forbidden_If_CustomerId_Missing()
    {
        var mockService = new Mock<IAccountService>();
        var attr = CreateAttributeWithService(mockService.Object);
        var context = CreateContext("/api/accounts/1", null);
        var executed = false;
        await attr.OnActionExecutionAsync(context, () => { executed = true; return Task.FromResult<ActionExecutedContext>(null); });
        Assert.IsType<ObjectResult>(context.Result);
        var result = context.Result as ObjectResult;
        Assert.Equal(StatusCodes.Status403Forbidden, result.StatusCode);
    }

    [Fact]
    public async Task Returns_Forbidden_If_Not_Authorized()
    {
        var mockService = new Mock<IAccountService>();
        mockService.Setup(s => s.GetListOfAccounts(100)).Returns(new List<Account> { new Account { AccountId = 2, CustomerId = 100 } });
        var attr = CreateAttributeWithService(mockService.Object);
        var context = CreateContext("/api/accounts/1", "100");
        context.HttpContext.RequestServices = new ServiceCollection().AddSingleton(mockService.Object).BuildServiceProvider();
        var executed = false;
        await attr.OnActionExecutionAsync(context, () => { executed = true; return Task.FromResult<ActionExecutedContext>(null); });
        Assert.IsType<ObjectResult>(context.Result);
        var result = context.Result as ObjectResult;
        Assert.Equal(StatusCodes.Status403Forbidden, result.StatusCode);
    }

    [Fact]
    public async Task Calls_Next_If_Authorized()
    {
        var mockService = new Mock<IAccountService>();
        mockService.Setup(s => s.GetListOfAccounts(100)).Returns(new List<Account> { new Account { AccountId = 1, CustomerId = 100 } });
        var attr = CreateAttributeWithService(mockService.Object);
        var context = CreateContext("/api/accounts/1", "100");
        context.HttpContext.RequestServices = new ServiceCollection().AddSingleton(mockService.Object).BuildServiceProvider();
        var called = false;
        await attr.OnActionExecutionAsync(context, () => { called = true; return Task.FromResult<ActionExecutedContext>(null); });
        Assert.True(called);
        Assert.Null(context.Result);
    }
}
