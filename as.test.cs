using Xunit;
using Moq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
using AccountsApi.Middleware;
using AccountsApi.Services;
using AccountsApi.Models;

namespace AccountsApi.Tests.Middleware
{
    public class AccountSecurityAttributeTests
    {
        private AccountSecurityAttribute CreateAttribute(IAccountService accountService = null)
        {
            var attr = new AccountSecurityAttribute();
            return attr;
        }

        private ActionExecutingContext CreateContext(string path, string customerIdHeader = null)
        {
            var httpContext = new DefaultHttpContext();
            httpContext.Request.Path = path;
            if (customerIdHeader != null)
                httpContext.Request.Headers["X-Customer-Id"] = customerIdHeader;
            var actionContext = new ActionContext(httpContext, new Microsoft.AspNetCore.Routing.RouteData(), new Microsoft.AspNetCore.Mvc.Abstractions.ActionDescriptor());
            return new ActionExecutingContext(actionContext, new List<IFilterMetadata>(), new Dictionary<string, object>(), null);
        }

        [Fact]
        public async Task OnActionExecutionAsync_MissingAccountIdOrCustomerId_ReturnsForbidden()
        {
            var attr = CreateAttribute();
            var context = CreateContext("/api/accounts/", null);
            var executed = false;
            await attr.OnActionExecutionAsync(context, () => { executed = true; return Task.FromResult<ActionExecutedContext>(null); });
            Assert.False(executed);
            var result = Assert.IsType<ObjectResult>(context.Result);
            Assert.Equal(StatusCodes.Status403Forbidden, result.StatusCode);
        }

        [Fact]
        public async Task OnActionExecutionAsync_InvalidAccountAccess_ReturnsForbidden()
        {
            var mockService = new Mock<IAccountService>();
            mockService.Setup(s => s.GetListOfAccounts(1)).Returns(new List<Account>());
            var attr = CreateAttribute();
            var context = CreateContext("/api/accounts/123", "1");
            context.HttpContext.RequestServices = new ServiceProviderStub(mockService.Object);
            var executed = false;
            await attr.OnActionExecutionAsync(context, () => { executed = true; return Task.FromResult<ActionExecutedContext>(null); });
            Assert.False(executed);
            var result = Assert.IsType<ObjectResult>(context.Result);
            Assert.Equal(StatusCodes.Status403Forbidden, result.StatusCode);
        }

        [Fact]
        public async Task OnActionExecutionAsync_ValidAccountAccess_CallsNext()
        {
            var mockService = new Mock<IAccountService>();
            mockService.Setup(s => s.GetListOfAccounts(1)).Returns(new List<Account> { new Account { AccountId = 123 } });
            var attr = CreateAttribute();
            var context = CreateContext("/api/accounts/123", "1");
            context.HttpContext.RequestServices = new ServiceProviderStub(mockService.Object);
            var executed = false;
            await attr.OnActionExecutionAsync(context, () => { executed = true; return Task.FromResult<ActionExecutedContext>(null); });
            Assert.True(executed);
            Assert.Null(context.Result);
        }

        // Helper for DI
        private class ServiceProviderStub : IServiceProvider
        {
            private readonly IAccountService _service;
            public ServiceProviderStub(IAccountService service) { _service = service; }
            public object GetService(System.Type serviceType)
            {
                if (serviceType == typeof(IAccountService)) return _service;
                return null;
            }
        }
    }
}
